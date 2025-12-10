import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=" * 60)
print("检查所有表的数据")
print("=" * 60)

# 检查关键表
tables_to_check = [
    ('event_management_venue', 'venue'),
    ('event_management_event', 'event'),
    ('event_management_group', 'group'),
    ('event_management_athleteevent', 'athlete_event'),
    ('result_management_result', 'result'),
    ('result_management_medalhonor', 'medal_honor'),
    ('data_statistics_datareport', 'data_report'),
]

for django_table, old_table in tables_to_check:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM "{django_table}"')
        django_count = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT COUNT(*) FROM "{old_table}"')
        old_count = cursor.fetchone()[0]
        
        print(f"{django_table:40} Django表: {django_count:3}  旧表: {old_count:3}")
    except Exception as e:
        print(f"{django_table:40} 错误: {str(e)[:50]}")

conn.close()

