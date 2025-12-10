"""
为数据库表字段添加默认值，解决NOT NULL约束问题
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
print("修复表默认值")
print("=" * 80)

try:
    # SQLite不支持直接修改列的默认值，但我们可以：
    # 1. 更新现有空值
    # 2. 在应用层处理
    
    # 更新team表的空值
    print("\n【更新basic_info_team表】")
    cursor.execute('''
        UPDATE basic_info_team
        SET 
            team_code = COALESCE(team_code, 
                CASE region 
                    WHEN "广州" THEN "GZ"
                    WHEN "深圳" THEN "SZ"
                    WHEN "香港" THEN "HK"
                    WHEN "澳门" THEN "MO"
                    ELSE "OT"
                END),
            sport_type = COALESCE(sport_type, "综合"),
            is_active = COALESCE(is_active, 1)
        WHERE team_code IS NULL OR team_code = "" 
           OR sport_type IS NULL OR sport_type = ""
           OR is_active IS NULL
    ''')
    updated = cursor.rowcount
    print(f"  ✓ 更新了 {updated} 条记录")
    
    # 更新athlete表的空值
    print("\n【更新basic_info_athlete表】")
    cursor.execute('''
        UPDATE basic_info_athlete
        SET id_card = COALESCE(id_card, "")
        WHERE id_card IS NULL
    ''')
    updated = cursor.rowcount
    print(f"  ✓ 更新了 {updated} 条记录")
    
    conn.commit()
    
    print("\n" + "=" * 80)
    print("修复完成！")
    print("=" * 80)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

