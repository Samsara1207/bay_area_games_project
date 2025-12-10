"""
直接使用SQL迁移数据，不依赖Django ORM
"""
import sqlite3
import os
from django.conf import settings

# 设置Django
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

db_path = settings.DATABASES['default']['NAME']
if not os.path.isabs(db_path):
    db_path = str(settings.BASE_DIR / db_path)
else:
    db_path = str(db_path)

print(f"数据库路径: {db_path}")

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 检查basic_info_team表结构
    cursor.execute('PRAGMA table_info("basic_info_team")')
    team_cols = {col[1]: col for col in cursor.fetchall()}
    print(f"\nbasic_info_team 表列: {list(team_cols.keys())}")
    
    # 检查team表结构
    cursor.execute('PRAGMA table_info("team")')
    old_team_cols = {col[1]: col for col in cursor.fetchall()}
    print(f"team 表列: {list(old_team_cols.keys())}")
    
    # 找到共同列（排除主键）
    common_cols = [col for col in old_team_cols.keys() if col in team_cols and col != 'team_id' and col != 'id']
    print(f"\n共同列: {common_cols}")
    
    # 清空新表
    cursor.execute('DELETE FROM "basic_info_team"')
    
    # 复制数据
    if common_cols:
        select_cols = ','.join([f'"{col}"' for col in common_cols])
        insert_cols = ','.join([f'"{col}"' for col in common_cols])
        
        # 如果目标表有team_code但源表没有，需要生成
        if 'team_code' in team_cols and 'team_code' not in common_cols:
            # 从region生成team_code
            # 添加team_code到insert
            insert_cols = insert_cols + ',"team_code"'
            # 修改select，添加CASE语句生成team_code
            select_cols = select_cols + ',CASE region WHEN "广州" THEN "01" WHEN "香港" THEN "03" WHEN "澳门" THEN "04" ELSE "00" END as team_code'
        
        # 处理其他必填字段
        required_cols = [col for col, info in team_cols.items() if info[3] == 1 and col != 'id' and col not in common_cols and col != 'team_code']
        for req_col in required_cols:
            if req_col == 'sport_type':
                insert_cols = insert_cols + ',"sport_type"'
                select_cols = select_cols + ',"田径" as sport_type'
            elif req_col == 'is_active':
                insert_cols = insert_cols + ',"is_active"'
                select_cols = select_cols + ',1 as is_active'
        
        sql = f'INSERT INTO "basic_info_team" ({insert_cols}) SELECT {select_cols} FROM "team"'
        print(f"\n执行SQL: {sql[:200]}...")
        cursor.execute(sql)
        conn.commit()
        
        cursor.execute('SELECT COUNT(*) FROM "basic_info_team"')
        count = cursor.fetchone()[0]
        print(f"\n✓ 已迁移 {count} 条 team 记录")
    
    # 迁移athlete
    cursor.execute('PRAGMA table_info("basic_info_athlete")')
    athlete_cols = {col[1]: col for col in cursor.fetchall()}
    
    cursor.execute('PRAGMA table_info("athlete")')
    old_athlete_cols = {col[1]: col for col in cursor.fetchall()}
    
    common_athlete_cols = [col for col in old_athlete_cols.keys() if col in athlete_cols and col != 'athlete_id' and col != 'id']
    
    # 建立team_id映射
    cursor.execute('SELECT team_id FROM "team" ORDER BY team_id')
    old_team_ids = [str(row[0]) for row in cursor.fetchall()]
    cursor.execute('SELECT id FROM "basic_info_team" ORDER BY id')
    new_team_ids = [row[0] for row in cursor.fetchall()]
    team_id_map = {}
    for i, old_id in enumerate(old_team_ids):
        if i < len(new_team_ids):
            team_id_map[old_id] = new_team_ids[i]
    
    # 清空新表
    cursor.execute('DELETE FROM "basic_info_athlete"')
    
    # 检查必填字段
    required_athlete_cols = [col for col, info in athlete_cols.items() if info[3] == 1 and col != 'id' and col not in common_athlete_cols]
    
    # 构建最终要插入的列（包括必填字段）
    final_cols = list(common_athlete_cols)
    for req_col in required_athlete_cols:
        if req_col not in final_cols:
            final_cols.append(req_col)
    
    # 复制数据
    if final_cols and 'team_id' in final_cols:
        # 构建SELECT语句
        select_parts = []
        for col in final_cols:
            if col == 'age' and 'birth_date' in old_athlete_cols:
                # 从birth_date计算age
                select_parts.append('(CAST(strftime("%Y", "now") AS INTEGER) - CAST(strftime("%Y", "birth_date") AS INTEGER)) as age')
            elif col in old_athlete_cols:
                select_parts.append(f'"{col}"')
            elif col == 'age':
                select_parts.append('25 as age')  # 默认年龄
            elif col == 'position':
                select_parts.append('"运动员" as position')  # 默认职位
            elif col == 'status':
                select_parts.append('"active" as status')  # 默认状态
            else:
                # 其他必填字段使用默认值
                select_parts.append(f'"" as {col}')  # 空字符串作为默认值
        
        select_cols = ','.join(select_parts)
        cursor.execute(f'SELECT {select_cols} FROM "athlete"')
        rows = cursor.fetchall()
        
        # 插入数据并映射team_id
        insert_cols = ','.join([f'"{col}"' for col in final_cols])
        placeholders = ','.join(['?' for _ in final_cols])
        
        for row in rows:
            row_list = list(row)
            # 确保行数据长度匹配
            while len(row_list) < len(final_cols):
                row_list.append(None)
            row_list = row_list[:len(final_cols)]
            
            row_dict = dict(zip(final_cols, row_list))
            
            # 映射team_id
            if 'team_id' in row_dict and row_dict['team_id']:
                old_team_id = str(row_dict['team_id'])
                if old_team_id in team_id_map:
                    team_id_idx = final_cols.index('team_id')
                    row_list[team_id_idx] = team_id_map[old_team_id]
                elif new_team_ids:
                    team_id_idx = final_cols.index('team_id')
                    row_list[team_id_idx] = new_team_ids[0]
                else:
                    continue
            
            cursor.execute(f'INSERT INTO "basic_info_athlete" ({insert_cols}) VALUES ({placeholders})', tuple(row_list))
        
        conn.commit()
        
        cursor.execute('SELECT COUNT(*) FROM "basic_info_athlete"')
        count = cursor.fetchone()[0]
        print(f"✓ 已迁移 {count} 条 athlete 记录")
    
    print("\n数据迁移完成！")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

