"""
从旧表同步代表队的leader信息
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
print("同步代表队leader信息")
print("=" * 80)

try:
    # 从旧表同步leader信息
    cursor.execute('''
        UPDATE basic_info_team
        SET 
            leader_name = COALESCE(
                (SELECT leader_name FROM team WHERE team.team_name = basic_info_team.team_name LIMIT 1),
                leader_name,
                ""
            ),
            leader_phone = COALESCE(
                (SELECT leader_phone FROM team WHERE team.team_name = basic_info_team.team_name LIMIT 1),
                leader_phone,
                ""
            ),
            city_code = COALESCE(
                (SELECT city_code FROM team WHERE team.team_name = basic_info_team.team_name LIMIT 1),
                city_code,
                CASE region 
                    WHEN "广州" THEN "01"
                    WHEN "深圳" THEN "02"
                    WHEN "香港" THEN "03"
                    WHEN "澳门" THEN "04"
                    ELSE "99"
                END
            )
        WHERE leader_name IS NULL OR leader_name = "" 
           OR leader_phone IS NULL OR leader_phone = ""
    ''')
    
    updated = cursor.rowcount
    conn.commit()
    print(f"  ✓ 更新了 {updated} 条记录")
    
    # 验证
    cursor.execute('SELECT team_name, leader_name, leader_phone FROM basic_info_team')
    teams = cursor.fetchall()
    print("\n更新后的代表队信息:")
    for team_name, leader_name, leader_phone in teams:
        print(f"  {team_name}: leader_name={leader_name or '-'}, leader_phone={leader_phone or '-'}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

