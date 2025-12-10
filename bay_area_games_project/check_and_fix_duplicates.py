"""
检查并修复重复的代表队
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
print("检查并修复重复的代表队")
print("=" * 80)

try:
    # 检查重复
    cursor.execute('''
        SELECT team_name, COUNT(*) as cnt, GROUP_CONCAT(id) as ids
        FROM basic_info_team
        GROUP BY team_name
        HAVING COUNT(*) > 1
    ''')
    duplicates = cursor.fetchall()
    
    if duplicates:
        print(f"\n找到 {len(duplicates)} 组重复的代表队:")
        for team_name, cnt, ids in duplicates:
            print(f"  {team_name}: {cnt} 条记录 (IDs: {ids})")
        
        # 删除重复，保留ID最小的
        print("\n删除重复记录...")
        for team_name, cnt, ids in duplicates:
            id_list = [int(x) for x in ids.split(',')]
            keep_id = min(id_list)
            delete_ids = [x for x in id_list if x != keep_id]
            
            # 更新运动员的team_id到保留的ID
            for delete_id in delete_ids:
                cursor.execute('''
                    UPDATE basic_info_athlete
                    SET team_id = ?
                    WHERE team_id = ?
                ''', (keep_id, delete_id))
            
            # 删除重复记录
            for delete_id in delete_ids:
                cursor.execute('DELETE FROM basic_info_team WHERE id = ?', (delete_id,))
                print(f"  ✓ 删除了ID {delete_id}，保留ID {keep_id}")
        
        conn.commit()
        print(f"\n  ✓ 已删除 {sum(len(ids.split(','))-1 for _, _, ids in duplicates)} 条重复记录")
    else:
        print("\n  ✓ 无重复的代表队")
    
    # 验证
    cursor.execute('SELECT COUNT(*) FROM basic_info_team')
    total = cursor.fetchone()[0]
    print(f"\n当前代表队总数: {total}")
    
    # 检查athletes_count
    cursor.execute('''
        SELECT t.id, t.team_name, COUNT(a.id) as athlete_count
        FROM basic_info_team t
        LEFT JOIN basic_info_athlete a ON a.team_id = t.id
        GROUP BY t.id, t.team_name
    ''')
    teams_with_count = cursor.fetchall()
    print("\n代表队及其运动员数量:")
    for team_id, team_name, count in teams_with_count:
        print(f"  {team_name} (ID: {team_id}): {count} 个运动员")
    
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()
finally:
    conn.close()

