"""
列出所有可以计算排名的项目ID
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

print("=" * 70)
print("可以计算排名的项目列表")
print("=" * 70)

# 查询所有有成绩记录的项目
cursor.execute('''
    SELECT DISTINCT 
        e.id,
        e.event_name,
        e.event_type,
        COUNT(r.id) as result_count
    FROM "event_management_event" e
    LEFT JOIN "event_management_athleteevent" ae ON ae.event_id = e.id
    LEFT JOIN "result_management_result" r ON r.apply_id = ae.id
    GROUP BY e.id, e.event_name, e.event_type
    HAVING COUNT(r.id) > 0
    ORDER BY e.id
''')

events = cursor.fetchall()

if events:
    print(f"\n找到 {len(events)} 个有成绩记录的项目：\n")
    print(f"{'项目ID':<10} {'项目名称':<30} {'项目类型':<20} {'成绩数':<10}")
    print("-" * 70)
    
    for event_id, event_name, event_type, result_count in events:
        print(f"{event_id:<10} {event_name:<30} {event_type:<20} {result_count:<10}")
    
    print("\n" + "=" * 70)
    print("使用说明：")
    print("=" * 70)
    print("在成绩管理页面，点击'计算排名'按钮，输入上述项目ID即可。")
    print("\n项目ID列表：")
    event_ids = [str(e[0]) for e in events]
    print(", ".join(event_ids))
else:
    print("\n暂无有成绩记录的项目")

# 查询所有项目（包括没有成绩的）
print("\n" + "=" * 70)
print("所有项目列表（包括无成绩的）")
print("=" * 70)

cursor.execute('''
    SELECT 
        e.id,
        e.event_name,
        e.event_type,
        COUNT(ae.id) as registration_count,
        COUNT(r.id) as result_count
    FROM "event_management_event" e
    LEFT JOIN "event_management_athleteevent" ae ON ae.event_id = e.id
    LEFT JOIN "result_management_result" r ON r.apply_id = ae.id
    GROUP BY e.id, e.event_name, e.event_type
    ORDER BY e.id
''')

all_events = cursor.fetchall()

if all_events:
    print(f"\n{'项目ID':<10} {'项目名称':<30} {'项目类型':<20} {'报名数':<10} {'成绩数':<10}")
    print("-" * 70)
    
    for event_id, event_name, event_type, reg_count, result_count in all_events:
        status = "有成绩" if result_count > 0 else "无成绩"
        print(f"{event_id:<10} {event_name:<30} {event_type:<20} {reg_count:<10} {result_count:<10} ({status})")

conn.close()

