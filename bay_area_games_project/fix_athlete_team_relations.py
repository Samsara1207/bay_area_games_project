"""
修复运动员与代表队的关联关系
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
print("修复运动员与代表队的关联")
print("=" * 80)

try:
    # 建立team_id映射（从旧表到新表）
    cursor.execute('SELECT team_id, team_name FROM "team" ORDER BY team_id')
    old_teams = cursor.fetchall()
    
    cursor.execute('SELECT id, team_name FROM "basic_info_team" ORDER BY id')
    new_teams = cursor.fetchall()
    
    # 创建映射：旧team_id -> 新team_id
    team_id_map = {}
    for old_id, old_name in old_teams:
        # 通过team_name匹配
        for new_id, new_name in new_teams:
            if old_name == new_name:
                team_id_map[old_id] = new_id
                break
    
    print(f"\n建立team_id映射: {len(team_id_map)} 个映射")
    
    # 更新运动员的team_id
    cursor.execute('SELECT athlete_id, team_id FROM "athlete"')
    old_athletes = cursor.fetchall()
    
    updated = 0
    for old_athlete_id, old_team_id in old_athletes:
        if old_team_id in team_id_map:
            new_team_id = team_id_map[old_team_id]
            # 通过athlete的name匹配到新表
            cursor.execute('SELECT name FROM "athlete" WHERE athlete_id = ?', (old_athlete_id,))
            athlete_name = cursor.fetchone()
            if athlete_name:
                cursor.execute('''
                    UPDATE basic_info_athlete
                    SET team_id = ?
                    WHERE name = ? AND (team_id IS NULL OR team_id = 0)
                ''', (new_team_id, athlete_name[0]))
                if cursor.rowcount > 0:
                    updated += 1
    
    conn.commit()
    print(f"  ✓ 更新了 {updated} 条运动员记录的team_id")
    
    # 验证
    cursor.execute('SELECT name, team_id FROM basic_info_athlete')
    athletes = cursor.fetchall()
    print("\n更新后的运动员关联:")
    for name, team_id in athletes:
        cursor.execute('SELECT team_name FROM basic_info_team WHERE id = ?', (team_id,))
        team_name = cursor.fetchone()
        print(f"  {name}: team_id={team_id}, team={team_name[0] if team_name else '无'}")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

