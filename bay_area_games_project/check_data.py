import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=" * 60)
print("检查数据库中的表和数据")
print("=" * 60)

# 检查所有包含 team 或 athlete 的表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name LIKE '%team%' OR name LIKE '%athlete%') ORDER BY name")
tables = [row[0] for row in cursor.fetchall()]

print("\n相关表:")
for table in tables:
    try:
        cursor.execute(f'SELECT COUNT(*) FROM "{table}"')
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} 条记录")
        
        # 如果是 team 或 athlete 表，显示前几条数据
        if 'team' in table.lower() and count > 0:
            cursor.execute(f'SELECT * FROM "{table}" LIMIT 3')
            rows = cursor.fetchall()
            print(f"    前3条数据示例:")
            for row in rows[:2]:
                print(f"      {row}")
        elif 'athlete' in table.lower() and count > 0:
            cursor.execute(f'SELECT * FROM "{table}" LIMIT 3')
            rows = cursor.fetchall()
            print(f"    前3条数据示例:")
            for row in rows[:2]:
                print(f"      {row}")
    except Exception as e:
        print(f"  {table}: 查询失败 - {e}")

conn.close()

