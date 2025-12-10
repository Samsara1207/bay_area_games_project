import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("检查 basic_info_team 表结构:")
cursor.execute('PRAGMA table_info("basic_info_team")')
cols = cursor.fetchall()
for c in cols:
    print(f"  {c[1]} ({c[2]}) - NOT NULL: {c[3]}")

conn.close()

