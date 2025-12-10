import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=" * 60)
print("检查 basic_info_team 表结构")
print("=" * 60)
cursor.execute('PRAGMA table_info("basic_info_team")')
cols = cursor.fetchall()
for col in cols:
    print(f"{col[1]:20} {col[2]:15} NOT NULL={col[3]} DEFAULT={col[4]}")

print("\n" + "=" * 60)
print("检查 basic_info_athlete 表结构")
print("=" * 60)
cursor.execute('PRAGMA table_info("basic_info_athlete")')
cols = cursor.fetchall()
for col in cols:
    print(f"{col[1]:20} {col[2]:15} NOT NULL={col[3]} DEFAULT={col[4]}")

conn.close()

