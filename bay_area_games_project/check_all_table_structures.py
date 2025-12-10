"""
检查所有Django表与旧表的字段差异
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

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 需要检查的表
tables_to_check = [
    ('basic_info_team', 'team'),
    ('basic_info_athlete', 'athlete'),
    ('result_management_result', 'result'),
    ('result_management_medalhonor', 'medal_honor'),
]

print("=" * 80)
print("检查表结构差异")
print("=" * 80)

for django_table, old_table in tables_to_check:
    print(f"\n【{django_table}】")
    
    # 检查Django表
    try:
        cursor.execute(f'PRAGMA table_info("{django_table}")')
        django_cols = {col[1]: col for col in cursor.fetchall()}
        print(f"  Django表列数: {len(django_cols)}")
    except Exception as e:
        print(f"  Django表不存在: {e}")
        django_cols = {}
    
    # 检查旧表
    try:
        cursor.execute(f'PRAGMA table_info("{old_table}")')
        old_cols = {col[1]: col for col in cursor.fetchall()}
        print(f"  旧表列数: {len(old_cols)}")
    except Exception as e:
        print(f"  旧表不存在: {e}")
        old_cols = {}
    
    # 找出差异
    if django_cols and old_cols:
        missing_in_django = set(old_cols.keys()) - set(django_cols.keys())
        missing_in_old = set(django_cols.keys()) - set(old_cols.keys())
        
        if missing_in_django:
            print(f"  旧表有但Django表没有: {missing_in_django}")
        if missing_in_old:
            print(f"  Django表有但旧表没有: {missing_in_old}")

conn.close()

