"""
补全代表队信息（领队、领队电话等）
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
print("补全代表队信息")
print("=" * 80)

try:
    # 从旧表读取完整信息
    cursor.execute('''
        SELECT team_name, region, city_code, leader_name, leader_phone, 
               doctor_name, doctor_phone, logo_url, accommodation, transport,
               uniform_custom, budget, insurance_no, physical_report_url
        FROM team
    ''')
    old_teams = cursor.fetchall()
    
    print(f"\n从旧表读取到 {len(old_teams)} 条代表队信息")
    
    # 更新新表
    updated = 0
    for team_data in old_teams:
        team_name, region, city_code, leader_name, leader_phone, doctor_name, doctor_phone, \
        logo_url, accommodation, transport, uniform_custom, budget, insurance_no, physical_report_url = team_data
        
        cursor.execute('''
            UPDATE basic_info_team
            SET 
                city_code = COALESCE(?, city_code, 
                    CASE region 
                        WHEN "广州" THEN "01"
                        WHEN "深圳" THEN "02"
                        WHEN "香港" THEN "03"
                        WHEN "澳门" THEN "04"
                        ELSE "99"
                    END),
                leader_name = COALESCE(?, leader_name, ""),
                leader_phone = COALESCE(?, leader_phone, ""),
                doctor_name = COALESCE(?, doctor_name),
                doctor_phone = COALESCE(?, doctor_phone),
                logo_url = COALESCE(?, logo_url),
                accommodation = COALESCE(?, accommodation),
                transport = COALESCE(?, transport),
                uniform_custom = COALESCE(?, uniform_custom),
                budget = COALESCE(?, budget),
                insurance_no = COALESCE(?, insurance_no),
                physical_report_url = COALESCE(?, physical_report_url)
            WHERE team_name = ?
        ''', (city_code, leader_name, leader_phone, doctor_name, doctor_phone,
              logo_url, accommodation, transport, uniform_custom, budget,
              insurance_no, physical_report_url, team_name))
        
        if cursor.rowcount > 0:
            updated += 1
            print(f"  ✓ 更新: {team_name}")
    
    conn.commit()
    print(f"\n  ✓ 共更新 {updated} 条记录")
    
    # 验证
    cursor.execute('SELECT team_name, leader_name, leader_phone FROM basic_info_team')
    teams = cursor.fetchall()
    print("\n更新后的代表队信息:")
    for team_name, leader_name, leader_phone in teams:
        print(f"  {team_name}:")
        print(f"    leader_name: {leader_name or '-'}")
        print(f"    leader_phone: {leader_phone or '-'}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

