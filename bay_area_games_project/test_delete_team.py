"""
测试删除代表队功能
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from basic_info.models import Team, Athlete

print("=" * 80)
print("测试删除代表队")
print("=" * 80)

# 检查初始的三个代表队
initial_teams = ['广东省广州市代表队', '中国香港代表队', '中国澳门代表队']

for team_name in initial_teams:
    try:
        team = Team.objects.get(team_name=team_name)
        athlete_count = team.athletes.count()
        print(f"\n{team_name}:")
        print(f"  ID: {team.id}")
        print(f"  关联运动员数: {athlete_count}")
        
        if athlete_count > 0:
            print(f"  ⚠ 有 {athlete_count} 个关联运动员，删除时会:")
            print(f"    - 如果on_delete=CASCADE: 运动员会被删除")
            print(f"    - 如果on_delete=SET_NULL: 运动员的team_id会被设为NULL")
            
            # 检查是否可以删除
            try:
                # 先查看运动员
                athletes = team.athletes.all()
                print(f"  关联的运动员:")
                for athlete in athletes:
                    print(f"    - {athlete.name} (ID: {athlete.id})")
            except Exception as e:
                print(f"  错误: {e}")
    except Team.DoesNotExist:
        print(f"\n{team_name}: 不存在")
    except Team.MultipleObjectsReturned:
        teams = Team.objects.filter(team_name=team_name)
        print(f"\n{team_name}: 存在 {teams.count()} 条重复记录")
        for team in teams:
            print(f"  ID {team.id}: {team.athletes.count()} 个运动员")

