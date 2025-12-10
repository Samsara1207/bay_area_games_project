"""
修复数据库表结构：删除旧表并重新创建
"""
import sqlite3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from django.conf import settings
from django.db import connection

db_path = settings.DATABASES['default']['NAME']
if not os.path.isabs(db_path):
    db_path = str(settings.BASE_DIR / db_path)
else:
    db_path = str(db_path)

print(f"数据库路径: {db_path}")

# 关闭Django连接
connection.close()

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 备份旧数据
    print("\n备份旧数据...")
    cursor.execute('SELECT * FROM "basic_info_team"')
    old_teams = cursor.fetchall()
    cursor.execute('PRAGMA table_info("basic_info_team")')
    old_team_cols = [col[1] for col in cursor.fetchall()]
    
    cursor.execute('SELECT * FROM "basic_info_athlete"')
    old_athletes = cursor.fetchall()
    cursor.execute('PRAGMA table_info("basic_info_athlete")')
    old_athlete_cols = [col[1] for col in cursor.fetchall()]
    
    print(f"  备份了 {len(old_teams)} 条team记录")
    print(f"  备份了 {len(old_athletes)} 条athlete记录")
    
    # 删除旧表
    print("\n删除旧表...")
    cursor.execute('DROP TABLE IF EXISTS "basic_info_athlete"')
    cursor.execute('DROP TABLE IF EXISTS "basic_info_team"')
    conn.commit()
    print("  ✓ 旧表已删除")
    
    conn.close()
    
    # 重新运行迁移
    print("\n重新创建表结构...")
    from django.core.management import call_command
    call_command('migrate', 'basic_info', verbosity=0)
    print("  ✓ 表结构已创建")
    
    # 重新连接并恢复数据
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 检查新表结构
    cursor.execute('PRAGMA table_info("basic_info_team")')
    new_team_cols = {col[1]: col for col in cursor.fetchall()}
    print(f"\n新team表列: {list(new_team_cols.keys())}")
    
    cursor.execute('PRAGMA table_info("basic_info_athlete")')
    new_athlete_cols = {col[1]: col for col in cursor.fetchall()}
    print(f"新athlete表列: {list(new_athlete_cols.keys())}")
    
    # 从旧表team恢复数据到新表
    print("\n恢复team数据...")
    if old_teams:
        # 找到共同列
        common_cols = [col for col in old_team_cols if col in new_team_cols and col != 'id']
        
        # 从原始team表读取数据
        read_conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
        read_cursor = read_conn.cursor()
        
        read_cursor.execute('SELECT * FROM "team"')
        source_teams = read_cursor.fetchall()
        read_cursor.execute('PRAGMA table_info("team")')
        source_team_cols = [col[1] for col in read_cursor.fetchall()]
        
        # 插入数据
        for row in source_teams:
            row_dict = dict(zip(source_team_cols, row))
            
            # 构建插入数据
            insert_data = {}
            for col in new_team_cols.keys():
                if col == 'id':
                    continue
                elif col == 'city_code' and 'city_code' not in row_dict:
                    # 从region生成
                    region = row_dict.get('region', '')
                    city_code_map = {'广州': '01', '香港': '03', '澳门': '04', '深圳': '02'}
                    insert_data[col] = city_code_map.get(region, '00')
                elif col in row_dict:
                    insert_data[col] = row_dict[col]
                elif col in ['leader_name', 'leader_phone']:
                    insert_data[col] = ''  # 默认值
                else:
                    insert_data[col] = None
            
            # 构建SQL
            cols = list(insert_data.keys())
            values = list(insert_data.values())
            placeholders = ','.join(['?' for _ in cols])
            cols_str = ','.join([f'"{col}"' for col in cols])
            
            cursor.execute(f'INSERT INTO "basic_info_team" ({cols_str}) VALUES ({placeholders})', values)
        
        conn.commit()
        read_conn.close()
        
        cursor.execute('SELECT COUNT(*) FROM "basic_info_team"')
        count = cursor.fetchone()[0]
        print(f"  ✓ 恢复了 {count} 条team记录")
    
    # 恢复athlete数据
    print("\n恢复athlete数据...")
    if old_athletes:
        # 建立team_id映射
        read_conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
        read_cursor = read_conn.cursor()
        
        read_cursor.execute('SELECT team_id FROM "team" ORDER BY team_id')
        old_team_ids = [str(row[0]) for row in read_cursor.fetchall()]
        cursor.execute('SELECT id FROM "basic_info_team" ORDER BY id')
        new_team_ids = [row[0] for row in cursor.fetchall()]
        team_id_map = {}
        for i, old_id in enumerate(old_team_ids):
            if i < len(new_team_ids):
                team_id_map[old_id] = new_team_ids[i]
        
        read_cursor.execute('SELECT * FROM "athlete"')
        source_athletes = read_cursor.fetchall()
        read_cursor.execute('PRAGMA table_info("athlete")')
        source_athlete_cols = [col[1] for col in read_cursor.fetchall()]
        
        for row in source_athletes:
            row_dict = dict(zip(source_athlete_cols, row))
            
            # 映射team_id
            if 'team_id' in row_dict and row_dict['team_id']:
                old_team_id = str(row_dict['team_id'])
                if old_team_id in team_id_map:
                    row_dict['team_id'] = team_id_map[old_team_id]
                elif new_team_ids:
                    row_dict['team_id'] = new_team_ids[0]
                else:
                    continue
            
            # 构建插入数据
            insert_data = {}
            for col in new_athlete_cols.keys():
                if col == 'id':
                    continue
                elif col == 'team_id' and 'team_id' in row_dict:
                    insert_data['team_id'] = row_dict['team_id']
                elif col in row_dict:
                    insert_data[col] = row_dict[col]
                else:
                    insert_data[col] = None
            
            # 构建SQL
            cols = list(insert_data.keys())
            values = list(insert_data.values())
            placeholders = ','.join(['?' for _ in cols])
            cols_str = ','.join([f'"{col}"' for col in cols])
            
            cursor.execute(f'INSERT INTO "basic_info_athlete" ({cols_str}) VALUES ({placeholders})', values)
        
        conn.commit()
        read_conn.close()
        
        cursor.execute('SELECT COUNT(*) FROM "basic_info_athlete"')
        count = cursor.fetchone()[0]
        print(f"  ✓ 恢复了 {count} 条athlete记录")
    
    print("\n" + "="*60)
    print("数据库结构修复完成！")
    print("="*60)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

