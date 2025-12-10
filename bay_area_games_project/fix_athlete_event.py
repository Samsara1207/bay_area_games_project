"""
修复athlete_event数据迁移
"""
import sqlite3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from django.conf import settings

db_path = settings.DATABASES['default']['NAME']
if not os.path.isabs(db_path):
    db_path = str(settings.BASE_DIR / db_path)
else:
    db_path = str(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
read_conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
read_cursor = read_conn.cursor()

try:
    print("修复 athlete_event 数据迁移...")
    
    # 建立ID映射
    # athlete_id映射
    read_cursor.execute('SELECT athlete_id FROM "athlete" ORDER BY athlete_id')
    old_athlete_ids = [str(r[0]) for r in read_cursor.fetchall()]
    cursor.execute('SELECT id FROM "basic_info_athlete" ORDER BY id')
    new_athlete_ids = [r[0] for r in cursor.fetchall()]
    athlete_id_map = {}
    for i, old_id in enumerate(old_athlete_ids):
        if i < len(new_athlete_ids):
            athlete_id_map[old_id] = new_athlete_ids[i]
    
    # event_id映射
    read_cursor.execute('SELECT event_id FROM "event" ORDER BY event_id')
    old_event_ids = [str(r[0]) for r in read_cursor.fetchall()]
    cursor.execute('SELECT id FROM "event_management_event" ORDER BY id')
    new_event_ids = [r[0] for r in cursor.fetchall()]
    event_id_map = {}
    for i, old_id in enumerate(old_event_ids):
        if i < len(new_event_ids):
            event_id_map[old_id] = new_event_ids[i]
    
    # group_id映射
    read_cursor.execute('SELECT group_id FROM "group" ORDER BY group_id')
    old_group_ids = [str(r[0]) for r in read_cursor.fetchall()]
    cursor.execute('SELECT id FROM "event_management_group" ORDER BY id')
    new_group_ids = [r[0] for r in cursor.fetchall()]
    group_id_map = {}
    for i, old_id in enumerate(old_group_ids):
        if i < len(new_group_ids):
            group_id_map[old_id] = new_group_ids[i]
    
    # 读取旧数据
    read_cursor.execute('SELECT * FROM "athlete_event"')
    rows = read_cursor.fetchall()
    read_cursor.execute('PRAGMA table_info("athlete_event")')
    old_cols = [c[1] for c in read_cursor.fetchall()]
    
    # 获取Django表列
    cursor.execute('PRAGMA table_info("event_management_athleteevent")')
    django_cols = {c[1]: c for c in cursor.fetchall()}
    
    # 清空表
    cursor.execute('DELETE FROM "event_management_athleteevent"')
    
    # 插入数据
    inserted = 0
    for row in rows:
        row_dict = dict(zip(old_cols, row))
        
        # 映射外键
        if 'athlete_id' in row_dict and row_dict['athlete_id']:
            old_id = str(row_dict['athlete_id'])
            if old_id in athlete_id_map:
                row_dict['athlete_id'] = athlete_id_map[old_id]
            elif new_athlete_ids:
                row_dict['athlete_id'] = new_athlete_ids[0]
            else:
                continue
        
        if 'event_id' in row_dict and row_dict['event_id']:
            old_id = str(row_dict['event_id'])
            if old_id in event_id_map:
                row_dict['event_id'] = event_id_map[old_id]
            elif new_event_ids:
                row_dict['event_id'] = new_event_ids[0]
            else:
                continue
        
        if 'group_id' in row_dict and row_dict['group_id']:
            old_id = str(row_dict['group_id'])
            if old_id in group_id_map:
                row_dict['group_id'] = group_id_map[old_id]
            elif new_group_ids:
                row_dict['group_id'] = new_group_ids[0]
            else:
                continue
        
        # 构建插入数据
        insert_data = {}
        for col in django_cols.keys():
            if col == 'id':
                continue
            elif col in row_dict:
                insert_data[col] = row_dict[col]
            elif col == 'apply_status':
                insert_data[col] = row_dict.get('apply_status', '已报名')
            else:
                insert_data[col] = None
        
        # 插入
        cols = list(insert_data.keys())
        values = list(insert_data.values())
        placeholders = ','.join(['?' for _ in cols])
        cols_str = ','.join([f'"{col}"' for col in cols])
        
        try:
            cursor.execute(f'INSERT INTO "event_management_athleteevent" ({cols_str}) VALUES ({placeholders})', values)
            inserted += 1
        except Exception as e:
            print(f"  跳过记录: {e}")
    
    conn.commit()
    print(f"  ✓ 已迁移 {inserted} 条 athlete_event 记录")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    read_conn.close()
    conn.close()

