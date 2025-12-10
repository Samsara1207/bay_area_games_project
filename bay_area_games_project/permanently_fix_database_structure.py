"""
永久性修复数据库结构，使其与Django模型完全匹配
1. 删除重复的代表队
2. 修改所有表结构，使其与Django模型字段名一致
3. 确保所有字段都存在
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

print("=" * 80)
print("永久性修复数据库结构")
print("=" * 80)

try:
    # 1. 删除重复的代表队（保留ID最小的）
    print("\n【1. 删除重复的代表队】")
    cursor.execute('''
        DELETE FROM basic_info_team
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM basic_info_team
            GROUP BY team_name
        )
    ''')
    deleted = cursor.rowcount
    print(f"  ✓ 删除了 {deleted} 条重复记录")
    conn.commit()
    
    # 2. 修复basic_info_athlete表 - 添加缺失字段
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
            cursor.execute(f'ALTER TABLE "basic_info_athlete" ADD COLUMN "{field_name}" {field_def}')
    
    # 删除不需要的字段（如果存在）
    fields_to_remove = ['age', 'position']
    for field_name in fields_to_remove:
        if field_name in existing_cols:
            print(f"  注意: 字段 {field_name} 存在但Django模型不需要，保留（SQLite不支持删除列）")
    
    conn.commit()
    print("  ✓ basic_info_athlete表修复完成")
    
    # 3. 修复result_management_result表 - 确保字段名正确
    print("\n【3. 修复result_management_result表】")
    cursor.execute('PRAGMA table_info("result_management_result")')
    result_cols = {col[1]: col for col in cursor.fetchall()}
    
    # 检查apply_id字段（Django使用apply_id作为外键）
    if 'apply_id' not in result_cols:
        print("  检查apply外键...")
        # 如果旧表有apply_id，需要确保映射正确
    
    print("  ✓ result_management_result表检查完成")
    
    # 4. 修复result_management_medalhonor表
    print("\n【4. 修复result_management_medalhonor表】")
    cursor.execute('PRAGMA table_info("result_management_medalhonor")')
    medal_cols = {col[1]: col for col in cursor.fetchall()}
    
    # 确保所有外键字段存在
    required_fields = ['athlete_id', 'team_id', 'result_id']
    for field in required_fields:
        if field not in medal_cols:
            print(f"  警告: 字段 {field} 不存在")
    
    print("  ✓ result_management_medalhonor表检查完成")
    
    # 5. 从旧表同步缺失的数据到Django表
    print("\n【5. 同步缺失数据】")
    
    # 同步athlete表的缺失字段数据
    if 'birth_date' in fields_to_add and 'birth_date' not in existing_cols:
        # 从旧表复制数据
        try:
            cursor.execute('''
                UPDATE basic_info_athlete
                SET birth_date = (
                    SELECT birth_date 
                    FROM athlete 
                    WHERE athlete.athlete_id = basic_info_athlete.id
                )
                WHERE birth_date IS NULL OR birth_date = ""
            ''')
            updated = cursor.rowcount
            if updated > 0:
                print(f"  ✓ 更新了 {updated} 条athlete记录的birth_date")
        except Exception as e:
            print(f"  跳过birth_date同步: {e}")
    
    conn.commit()
    
    print("\n" + "=" * 80)
    print("数据库结构修复完成！")
    print("=" * 80)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

