"""
重置basic_info表：删除迁移记录并重新创建
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

print(f"数据库路径: {db_path}")

connection.close()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 删除迁移记录
    print("删除basic_info的迁移记录...")
    cursor.execute('DELETE FROM django_migrations WHERE app = "basic_info"')
    conn.commit()
    print("  ✓ 迁移记录已删除")
    
    conn.close()
    
    # 重新运行迁移
    print("\n重新创建表结构...")
    from django.core.management import call_command
    call_command('migrate', 'basic_info', verbosity=1)
    print("  ✓ 表结构已创建")
    
    # 验证表结构
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('PRAGMA table_info("basic_info_team")')
    team_cols = cursor.fetchall()
    print(f"\nbasic_info_team 表有 {len(team_cols)} 个列")
    
    cursor.execute('PRAGMA table_info("basic_info_athlete")')
    athlete_cols = cursor.fetchall()
    print(f"basic_info_athlete 表有 {len(athlete_cols)} 个列")
    
    print("\n" + "="*60)
    print("表结构已重新创建！现在可以运行数据迁移了。")
    print("="*60)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()

