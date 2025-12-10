"""
修复basic_info_team表结构，添加缺失的字段
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

try:
    print("检查并修复 basic_info_team 表结构...")
    
    # 检查当前列
    cursor.execute('PRAGMA table_info("basic_info_team")')
    existing_cols = {col[1]: col for col in cursor.fetchall()}
    
    # 需要添加的字段
    fields_to_add = {
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
    
    # 添加缺失的字段
    for field_name, field_def in fields_to_add.items():
        if field_name not in existing_cols:
            print(f"  添加字段: {field_name}")
            try:
                cursor.execute(f'ALTER TABLE "basic_info_team" ADD COLUMN "{field_name}" {field_def}')
            except Exception as e:
                print(f"    警告: {e}")
    
    # 如果city_code是NOT NULL但没有默认值，需要先更新现有数据
    if 'city_code' in existing_cols:
        # 检查是否有空值
        cursor.execute('SELECT COUNT(*) FROM "basic_info_team" WHERE city_code IS NULL OR city_code = ""')
        null_count = cursor.fetchone()[0]
        if null_count > 0:
            print(f"  更新 {null_count} 条记录的 city_code...")
            cursor.execute('''
                UPDATE "basic_info_team" 
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
    print("  ✓ 表结构修复完成")
    
    # 验证
    cursor.execute('PRAGMA table_info("basic_info_team")')
    final_cols = [col[1] for col in cursor.fetchall()]
    print(f"\n当前表列数: {len(final_cols)}")
    print(f"列名: {', '.join(final_cols)}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

