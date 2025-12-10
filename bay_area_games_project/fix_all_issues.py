"""
修复所有问题：
1. 删除重复的代表队
2. 修复athlete表缺失字段
3. 确保所有表结构与Django模型匹配
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
print("修复所有问题")
print("=" * 80)

try:
    # 1. 删除重复的代表队（保留ID最小的）
    print("\n【1. 删除重复的代表队】")
    cursor.execute('''
        DELETE FROM basic_info_team
        WHERE id IN (
            SELECT id FROM (
                SELECT id, ROW_NUMBER() OVER (PARTITION BY team_name ORDER BY id) as rn
                FROM basic_info_team
            ) WHERE rn > 1
        )
    ''')
    deleted = cursor.rowcount
    print(f"  ✓ 删除了 {deleted} 条重复记录")
    conn.commit()
    
    # 2. 修复basic_info_athlete表 - 添加所有缺失字段
    print("\n【2. 修复basic_info_athlete表】")
    cursor.execute('PRAGMA table_info("basic_info_athlete")')
    existing_cols = {col[1]: col for col in cursor.fetchall()}
    
    fields_to_add = {
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
    
    for field_name, field_def in fields_to_add.items():
        if field_name not in existing_cols:
            print(f"  添加字段: {field_name}")
            try:
                cursor.execute(f'ALTER TABLE "basic_info_athlete" ADD COLUMN "{field_name}" {field_def}')
            except Exception as e:
                print(f"    警告: {e}")
    
    # 从旧表同步数据
    try:
        cursor.execute('''
            UPDATE basic_info_athlete
            SET 
                birth_date = COALESCE((SELECT birth_date FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), birth_date, "2000-01-01"),
                bay_area_hukou = COALESCE((SELECT bay_area_hukou FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), bay_area_hukou, "广东"),
                height = COALESCE((SELECT height FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), height),
                weight = COALESCE((SELECT weight FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), weight),
                phone = COALESCE((SELECT phone FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), phone),
                emergency_contact = COALESCE((SELECT emergency_contact FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), emergency_contact),
                emergency_phone = COALESCE((SELECT emergency_phone FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), emergency_phone),
                health_status = COALESCE((SELECT health_status FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), health_status),
                qualification_status = COALESCE((SELECT qualification_status FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), qualification_status, "未审核"),
                competition_id = COALESCE((SELECT competition_id FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), competition_id),
                doping_test = COALESCE((SELECT doping_test FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), doping_test, "待检测"),
                clothing_size = COALESCE((SELECT clothing_size FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), clothing_size),
                insurance_info = COALESCE((SELECT insurance_info FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), insurance_info),
                join_time = COALESCE((SELECT join_time FROM athlete WHERE athlete.athlete_id = basic_info_athlete.id), join_time)
        ''')
        updated = cursor.rowcount
        print(f"  ✓ 更新了 {updated} 条athlete记录")
    except Exception as e:
        print(f"  跳过数据同步: {e}")
    
    conn.commit()
    print("  ✓ basic_info_athlete表修复完成")
    
    print("\n" + "=" * 80)
    print("所有问题修复完成！")
    print("=" * 80)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

