"""
简单直接的数据迁移脚本
"""
import sqlite3
from django.db import connection
from basic_info.models import Team, Athlete

# 关闭Django连接
connection.close()

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("开始迁移数据...")

# 1. 迁移 team 数据
print("\n1. 迁移 team 数据...")
cursor.execute('SELECT * FROM "team"')
team_rows = cursor.fetchall()
cursor.execute('PRAGMA table_info("team")')
team_cols = [col[1] for col in cursor.fetchall()]

print(f"  找到 {len(team_rows)} 条 team 记录")

# 清空Django表
Team.objects.all().delete()

# 插入数据
for row in team_rows:
    row_dict = dict(zip(team_cols, row))
    # 移除主键
    if 'team_id' in row_dict:
        del row_dict['team_id']
    
    # 只保留Django模型中存在的字段
    team_data = {}
    for field in Team._meta.get_fields():
        if hasattr(field, 'column') and field.column in row_dict:
            value = row_dict[field.column]
            # 处理日期时间
            if hasattr(field, 'get_internal_type') and field.get_internal_type() in ['DateTimeField', 'DateField']:
                if value:
                    from django.utils.dateparse import parse_datetime, parse_date
                    if field.get_internal_type() == 'DateTimeField':
                        value = parse_datetime(value) if isinstance(value, str) else value
                    else:
                        value = parse_date(value) if isinstance(value, str) else value
            team_data[field.name] = value
    
    try:
        Team.objects.create(**team_data)
    except Exception as e:
        print(f"  跳过记录（错误: {e}）")

print(f"  ✓ 已迁移 {Team.objects.count()} 条 team 记录")

# 2. 迁移 athlete 数据
print("\n2. 迁移 athlete 数据...")
cursor.execute('SELECT * FROM "athlete"')
athlete_rows = cursor.fetchall()
cursor.execute('PRAGMA table_info("athlete")')
athlete_cols = [col[1] for col in cursor.fetchall()]

print(f"  找到 {len(athlete_rows)} 条 athlete 记录")

# 建立team_id映射
cursor.execute('SELECT team_id FROM "team" ORDER BY team_id')
old_team_ids = [str(row[0]) for row in cursor.fetchall()]
new_teams = list(Team.objects.all().order_by('id'))
team_id_map = {}
for i, old_id in enumerate(old_team_ids):
    if i < len(new_teams):
        team_id_map[old_id] = new_teams[i]

# 清空Django表
Athlete.objects.all().delete()

# 插入数据
for row in athlete_rows:
    row_dict = dict(zip(athlete_cols, row))
    # 移除主键
    if 'athlete_id' in row_dict:
        del row_dict['athlete_id']
    
    # 映射team_id
    if 'team_id' in row_dict and row_dict['team_id']:
        old_team_id = str(row_dict['team_id'])
        if old_team_id in team_id_map:
            row_dict['team'] = team_id_map[old_team_id]
        elif new_teams:
            row_dict['team'] = new_teams[0]
        else:
            continue
        del row_dict['team_id']
    
    # 只保留Django模型中存在的字段
    athlete_data = {}
    for field in Athlete._meta.get_fields():
        if hasattr(field, 'column') and field.column in row_dict:
            value = row_dict[field.column]
            # 处理日期时间
            if hasattr(field, 'get_internal_type') and field.get_internal_type() in ['DateTimeField', 'DateField']:
                if value:
                    from django.utils.dateparse import parse_datetime, parse_date
                    if field.get_internal_type() == 'DateTimeField':
                        value = parse_datetime(value) if isinstance(value, str) else value
                    else:
                        value = parse_date(value) if isinstance(value, str) else value
            athlete_data[field.name] = value
    
    try:
        Athlete.objects.create(**athlete_data)
    except Exception as e:
        print(f"  跳过记录（错误: {e}）")

print(f"  ✓ 已迁移 {Athlete.objects.count()} 条 athlete 记录")

conn.close()
print("\n迁移完成！")

