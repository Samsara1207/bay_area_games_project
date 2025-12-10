"""
检查删除约束，找出为什么不能删除初始的三个队
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

print("=" * 80)
print("检查删除约束")
print("=" * 80)

initial_teams = ['广东省广州市代表队', '中国香港代表队', '中国澳门代表队']

for team_name in initial_teams:
    try:
        team = Team.objects.get(team_name=team_name)
        print(f"\n【{team_name}】")
        print(f"  Team ID: {team.id}")
        
        # 检查关联的运动员
        athletes = Athlete.objects.filter(team=team)
        print(f"  关联运动员数: {athletes.count()}")
        if athletes.exists():
            print(f"  运动员列表:")
            for athlete in athletes:
                print(f"    - {athlete.name} (ID: {athlete.id})")
        
        # 检查是否有其他表引用
        from event_management.models import AthleteEvent
        from result_management.models import Result, MedalHonor
        
        athlete_ids = list(athletes.values_list('id', flat=True))
        if athlete_ids:
            # 检查athlete_event
            events = AthleteEvent.objects.filter(athlete_id__in=athlete_ids)
            print(f"  关联的报名记录: {events.count()}")
            
            # 检查result
            apply_ids = list(events.values_list('id', flat=True))
            if apply_ids:
                results = Result.objects.filter(apply_id__in=apply_ids)
                print(f"  关联的成绩记录: {results.count()}")
                
                # 检查medal_honor
                result_ids = list(results.values_list('id', flat=True))
                if result_ids:
                    medals = MedalHonor.objects.filter(result_id__in=result_ids)
                    print(f"  关联的奖牌记录: {medals.count()}")
        
        # 尝试删除（不实际删除，只检查）
        print(f"\n  删除测试:")
        try:
            # 检查是否可以删除（不实际删除）
            if athletes.exists():
                print(f"    ⚠ 有 {athletes.count()} 个关联运动员")
                print(f"    删除此代表队会同时删除这些运动员（CASCADE）")
                print(f"    如果这些运动员有报名/成绩/奖牌记录，也会被删除")
            else:
                print(f"    ✓ 无关联运动员，可以安全删除")
        except Exception as e:
            print(f"    错误: {e}")
            
    except Team.DoesNotExist:
        print(f"\n【{team_name}】不存在")
    except Team.MultipleObjectsReturned:
        teams = Team.objects.filter(team_name=team_name)
        print(f"\n【{team_name}】存在 {teams.count()} 条重复记录")
        for team in teams:
            print(f"  ID {team.id}: {team.athletes.count()} 个运动员")

