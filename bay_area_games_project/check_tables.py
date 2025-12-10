import sqlite3

# 检查源数据库
print("=" * 50)
print("源数据库 (bay_area_games.db) 的表:")
print("=" * 50)
conn = sqlite3.connect('bay_area_games.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
source_tables = [row[0] for row in cursor.fetchall()]
for table in source_tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} 条记录")
    except Exception as e:
        print(f"  {table}: 查询失败 - {e}")
conn.close()

print("\n" + "=" * 50)
print("目标数据库 (db.sqlite3) 的表:")
print("=" * 50)
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
target_tables = [row[0] for row in cursor.fetchall()]
for table in target_tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"  {table}: {count} 条记录")
conn.close()

