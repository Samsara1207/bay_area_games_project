"""
修复数据库约束，使其与Django模型一致
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

print("=" * 80)
print("修复数据库约束")
print("=" * 80)

try:
    # SQLite不支持直接修改列约束，需要重建表
    # 但我们可以先检查并更新现有数据，然后修改表结构
    
    # 1. 修复basic_info_team表 - 确保team_code可以为空
    print("\n【修复basic_info_team表】")
    
    # 检查当前约束
    cursor.execute('PRAGMA table_info("basic_info_team")')
    cols = {col[1]: col for col in cursor.fetchall()}
    
    # 如果team_code是NOT NULL，需要更新空值为默认值
    if 'team_code' in cols and cols['team_code'][3] == 1:  # NOT NULL
        print("  更新team_code空值...")
        cursor.execute('''
            UPDATE basic_info_team
            SET team_code = CASE 
                WHEN region = "广州" THEN "GZ"
                WHEN region = "深圳" THEN "SZ"
                WHEN region = "香港" THEN "HK"
                WHEN region = "澳门" THEN "MO"
                ELSE "OT"
            END
            WHERE team_code IS NULL OR team_code = ""
        ''')
        conn.commit()
        print("  ✓ team_code已更新")
    
    # 2. 修复basic_info_athlete表 - 确保id_card可以为空
    print("\n【修复basic_info_athlete表】")
    
    cursor.execute('PRAGMA table_info("basic_info_athlete")')
    cols = {col[1]: col for col in cursor.fetchall()}
    
    # 如果id_card是NOT NULL，需要更新空值为空字符串
    if 'id_card' in cols and cols['id_card'][3] == 1:  # NOT NULL
        print("  更新id_card空值...")
        cursor.execute('''
            UPDATE basic_info_athlete
            SET id_card = ""
            WHERE id_card IS NULL
        ''')
        conn.commit()
        print("  ✓ id_card已更新")
    
    print("\n" + "=" * 80)
    print("注意：SQLite不支持直接修改列约束。")
    print("如果仍有问题，需要重建表或使用ALTER TABLE添加默认值。")
    print("=" * 80)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

