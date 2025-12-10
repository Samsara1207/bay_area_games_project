"""
永久性修复数据库结构脚本
在恢复数据库后运行此脚本，确保所有字段与Django模型匹配

使用方法: python fix_database_permanently.py
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
print("永久性修复数据库结构")
print("=" * 80)

try:
    # 1. 修复basic_info_team表
    print("\n【修复basic_info_team表】")
    cursor.execute('PRAGMA table_info("basic_info_team")')
    existing_cols = {col[1]: col for col in cursor.fetchall()}
    
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
    
    added = 0
    for field_name, field_def in team_fields.items():
        if field_name not in existing_cols:
            try:
                cursor.execute(f'ALTER TABLE "basic_info_team" ADD COLUMN "{field_name}" {field_def}')
                added += 1
                print(f"  ✓ 添加字段: {field_name}")
            except Exception as e:
                print(f"  ✗ 添加字段失败 {field_name}: {e}")
    
    if added > 0:
        conn.commit()
        print(f"  ✓ 共添加 {added} 个字段")
    else:
        print("  ✓ 所有字段已存在")
    
    # 更新city_code默认值
    try:
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
        conn.commit()
    except Exception:
        pass
    
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
    
    added = 0
    for field_name, field_def in athlete_fields.items():
        if field_name not in existing_cols:
            try:
                cursor.execute(f'ALTER TABLE "basic_info_athlete" ADD COLUMN "{field_name}" {field_def}')
                added += 1
                print(f"  ✓ 添加字段: {field_name}")
            except Exception as e:
                print(f"  ✗ 添加字段失败 {field_name}: {e}")
    
    if added > 0:
        conn.commit()
        print(f"  ✓ 共添加 {added} 个字段")
    else:
        print("  ✓ 所有字段已存在")
    
    print("\n" + "=" * 80)
    print("修复完成！现在可以正常使用API了。")
    print("=" * 80)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

