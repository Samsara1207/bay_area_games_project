import sqlite3

# 检查几个关键表的列名差异
conn = sqlite3.connect('bay_area_games.db')
cursor = conn.cursor()

tables_to_check = ['team', 'athlete', 'event', 'result']

for table in tables_to_check:
    print(f"\n表: {table}")
    print("-" * 50)
    try:
        cursor.execute(f'PRAGMA table_info("{table}")')
        columns = cursor.fetchall()
        print("源数据库列名:")
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    except Exception as e:
        print(f"错误: {e}")

conn.close()

print("\n" + "=" * 50)
print("目标数据库列名:")
print("=" * 50)

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

target_tables = {
    'team': 'basic_info_team',
    'athlete': 'basic_info_athlete',
    'event': 'event_management_event',
    'result': 'result_management_result',
}

for source_table, target_table in target_tables.items():
    print(f"\n表: {source_table} -> {target_table}")
    print("-" * 50)
    try:
        cursor.execute(f'PRAGMA table_info("{target_table}")')
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    except Exception as e:
        print(f"错误: {e}")

conn.close()

