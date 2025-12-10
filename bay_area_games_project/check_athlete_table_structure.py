"""
检查athlete表结构，找出所有NOT NULL字段
"""
import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

print("=" * 80)
print("检查basic_info_athlete表结构")
print("=" * 80)

cursor.execute('PRAGMA table_info("basic_info_athlete")')
cols = cursor.fetchall()

print("\n所有字段:")
for col in cols:
    col_name = col[1]
    col_type = col[2]
    not_null = col[3]
    default = col[4]
    print(f"  {col_name:20} {col_type:15} NOT NULL={not_null:5} DEFAULT={default}")

print("\nNOT NULL字段（需要默认值）:")
for col in cols:
    if col[3] == 1 and col[4] is None:  # NOT NULL且无默认值
        print(f"  - {col[1]} ({col[2]})")

conn.close()

