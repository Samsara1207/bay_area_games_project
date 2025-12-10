"""
确保所有Django模型需要的字段在数据库表中都存在
这是永久性修复，确保数据库结构与模型完全匹配
"""
import sqlite3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from django.conf import settings
from basic_info.models import Team, Athlete

db_path = settings.DATABASES['default']['NAME']
if not os.path.isabs(db_path):
    db_path = str(settings.BASE_DIR / db_path)
else:
    db_path = str(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("确保所有字段存在（永久性修复）")
print("=" * 80)

try:
    # 1. 修复basic_info_team表
    print("\n【修复basic_info_team表】")
    cursor.execute('PRAGMA table_info("basic_info_team")')
    existing_cols = {col[1]: col for col in cursor.fetchall()}
    
    # Django模型中的所有字段
    team_fields = {
        'city_code': 'varchar(6) NOT NULL DEFAULT ""',
        'leader_name': 'varchar(50) NOT NULL DEFAULT ""',
        'leader_phone': 'varchar(20) NOT NULL DEFAULT ""',
        'doctor_name': 'varchar(50) NULL',
        'doctor_phone': 'varchar(20) NULL',
        'logo_url': 'varchar(255) NULL',
        'accommodation': 'varchar(255) NULL',
        'transport': 'varchar(255) NULL',
        'uniform_custom': 'varchar(255) NULL',
        'budget': 'decimal NULL',
        'insurance_no': 'varchar(50) NULL',
        'physical_report_url': 'varchar(255) NULL',
    }
    
    for field_name, field_def in team_fields.items():
        if field_name not in existing_cols:
            print(f"  添加字段: {field_name}")
            try:
                cursor.execute(f'ALTER TABLE "basic_info_team" ADD COLUMN "{field_name}" {field_def}')
            except Exception as e:
                print(f"    错误: {e}")
    
    # 更新city_code的默认值
    cursor.execute('''
        UPDATE basic_info_team
        SET city_code = CASE 
            WHEN region = "广州" THEN "01"
            WHEN region = "深圳" THEN "02"
            WHEN region = "香港" THEN "03"
            WHEN region = "澳门" THEN "04"
            ELSE "99"
        END
        WHERE city_code IS NULL OR city_code = ""
    ''')
    
    # 更新leader_name和leader_phone的默认值（从旧表同步）
    try:
        cursor.execute('''
            UPDATE basic_info_team
            SET 
                leader_name = COALESCE((SELECT leader_name FROM team WHERE team.team_name = basic_info_team.team_name LIMIT 1), leader_name, ""),
                leader_phone = COALESCE((SELECT leader_phone FROM team WHERE team.team_name = basic_info_team.team_name LIMIT 1), leader_phone, "")
            WHERE leader_name IS NULL OR leader_name = "" OR leader_phone IS NULL OR leader_phone = ""
        ''')
    except Exception as e:
        print(f"  跳过leader数据同步: {e}")
    
    conn.commit()
    print("  ✓ basic_info_team表修复完成")
    
    # 2. 修复basic_info_athlete表
    print("\n【修复basic_info_athlete表】")
    cursor.execute('PRAGMA table_info("basic_info_athlete")')
    existing_cols = {col[1]: col for col in cursor.fetchall()}
    
    athlete_fields = {
        'birth_date': 'date NOT NULL DEFAULT "2000-01-01"',
        'emergency_phone': 'varchar(20) NULL',
        'weight': 'decimal NULL',
        'join_time': 'datetime NULL',
        'bay_area_hukou': 'varchar(10) NOT NULL DEFAULT "广东"',
        'doping_test': 'varchar(10) NOT NULL DEFAULT "待检测"',
        'health_status': 'varchar(100) NULL',
        'qualification_status': 'varchar(10) NOT NULL DEFAULT "未审核"',
        'emergency_contact': 'varchar(50) NULL',
        'height': 'decimal NULL',
        'competition_id': 'varchar(30) NULL',
        'past_records': 'text NULL',
        'clothing_size': 'varchar(20) NULL',
        'insurance_info': 'varchar(255) NULL',
    }
    
    for field_name, field_def in athlete_fields.items():
        if field_name not in existing_cols:
            print(f"  添加字段: {field_name}")
            try:
                cursor.execute(f'ALTER TABLE "basic_info_athlete" ADD COLUMN "{field_name}" {field_def}')
            except Exception as e:
                print(f"    错误: {e}")
    
    conn.commit()
    print("  ✓ basic_info_athlete表修复完成")
    
    # 3. 验证
    print("\n【验证】")
    cursor.execute('PRAGMA table_info("basic_info_team")')
    team_cols = [col[1] for col in cursor.fetchall()]
    required_team_fields = ['city_code', 'leader_name', 'leader_phone']
    missing_team = [f for f in required_team_fields if f not in team_cols]
    if missing_team:
        print(f"  ✗ basic_info_team缺失字段: {missing_team}")
    else:
        print("  ✓ basic_info_team所有必需字段存在")
    
    cursor.execute('PRAGMA table_info("basic_info_athlete")')
    athlete_cols = [col[1] for col in cursor.fetchall()]
    required_athlete_fields = ['birth_date', 'bay_area_hukou', 'qualification_status']
    missing_athlete = [f for f in required_athlete_fields if f not in athlete_cols]
    if missing_athlete:
        print(f"  ✗ basic_info_athlete缺失字段: {missing_athlete}")
    else:
        print("  ✓ basic_info_athlete所有必需字段存在")
    
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

