"""
手动创建basic_info表结构
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

print(f"数据库路径: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # 创建basic_info_team表
    print("创建 basic_info_team 表...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "basic_info_team" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "team_name" varchar(100) NOT NULL,
            "region" varchar(50) NOT NULL,
            "city_code" varchar(6) NOT NULL,
            "leader_name" varchar(50) NOT NULL,
            "leader_phone" varchar(20) NOT NULL,
            "doctor_name" varchar(50) NULL,
            "doctor_phone" varchar(20) NULL,
            "logo_url" varchar(255) NULL,
            "accommodation" varchar(255) NULL,
            "transport" varchar(255) NULL,
            "uniform_custom" varchar(255) NULL,
            "budget" decimal NULL,
            "insurance_no" varchar(50) NULL,
            "physical_report_url" varchar(255) NULL,
            "create_time" datetime NOT NULL,
            "update_time" datetime NOT NULL
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS "idx_team_region" ON "basic_info_team" ("region")')
    cursor.execute('CREATE INDEX IF NOT EXISTS "idx_team_city_code" ON "basic_info_team" ("city_code")')
    
    # 创建basic_info_athlete表
    print("创建 basic_info_athlete 表...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "basic_info_athlete" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" varchar(50) NOT NULL,
            "gender" varchar(2) NOT NULL,
            "birth_date" date NOT NULL,
            "id_card" varchar(30) NULL,
            "bay_area_hukou" varchar(10) NOT NULL,
            "height" decimal NULL,
            "weight" decimal NULL,
            "phone" varchar(20) NULL,
            "emergency_contact" varchar(50) NULL,
            "emergency_phone" varchar(20) NULL,
            "health_status" varchar(100) NULL,
            "qualification_status" varchar(10) NOT NULL DEFAULT '未审核',
            "competition_id" varchar(30) NULL UNIQUE,
            "past_records" text NULL,
            "doping_test" varchar(10) NOT NULL DEFAULT '待检测',
            "clothing_size" varchar(20) NULL,
            "insurance_info" varchar(255) NULL,
            "join_time" datetime NULL,
            "create_time" datetime NOT NULL,
            "update_time" datetime NOT NULL,
            "team_id" bigint NOT NULL REFERENCES "basic_info_team" ("id") DEFERRABLE INITIALLY DEFERRED
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS "idx_athlete_team" ON "basic_info_athlete" ("team_id")')
    cursor.execute('CREATE INDEX IF NOT EXISTS "idx_athlete_hukou" ON "basic_info_athlete" ("bay_area_hukou")')
    cursor.execute('CREATE INDEX IF NOT EXISTS "idx_athlete_qual" ON "basic_info_athlete" ("qualification_status")')
    
    conn.commit()
    print("  ✓ 表结构已创建")
    
    # 标记迁移为已应用
    print("\n标记迁移为已应用...")
    cursor.execute('''
        INSERT OR IGNORE INTO django_migrations (app, name, applied)
        VALUES ('basic_info', '0001_initial', datetime('now'))
    ''')
    conn.commit()
    print("  ✓ 迁移已标记")
    
    print("\n" + "="*60)
    print("表结构创建完成！")
    print("="*60)
    
except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

