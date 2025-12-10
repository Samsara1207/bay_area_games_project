"""
验证所有修复
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from basic_info.models import Team, Athlete
from basic_info.serializers import TeamSerializer, AthleteSerializer

print("=" * 80)
print("验证修复结果")
print("=" * 80)

# 1. 验证代表队
print("\n【验证代表队】")
teams = Team.objects.all()
print(f"  代表队数量: {teams.count()}")

for team in teams[:3]:
    serializer = TeamSerializer(team)
    data = serializer.data
    print(f"  {team.team_name}:")
    print(f"    - region: {data.get('region', '-')}")
    print(f"    - leader_name: {data.get('leader_name', '-')}")
    print(f"    - leader_phone: {data.get('leader_phone', '-')}")
    print(f"    - athletes_count: {data.get('athletes_count', 0)}")

# 2. 验证运动员
print("\n【验证运动员】")
athletes = Athlete.objects.all()
print(f"  运动员数量: {athletes.count()}")

for athlete in athletes[:3]:
    serializer = AthleteSerializer(athlete)
    data = serializer.data
    print(f"  {athlete.name}:")
    print(f"    - team_name: {data.get('team_name', '-')}")
    print(f"    - qualification_status: {data.get('qualification_status', '-')}")

# 3. 测试创建
print("\n【测试创建功能】")
try:
    # 测试创建代表队
    team_data = {
        'team_name': '测试队',
        'region': '深圳',
        'city_code': '02',
        'leader_name': '测试',
        'leader_phone': '13800000000',
    }
    team_serializer = TeamSerializer(data=team_data)
    if team_serializer.is_valid():
        test_team = team_serializer.save()
        print(f"  ✓ 代表队创建成功: {test_team.team_name}")
        test_team.delete()
        print("  ✓ 测试数据已删除")
    else:
        print(f"  ✗ 代表队创建失败: {team_serializer.errors}")
    
    # 测试创建运动员
    team = Team.objects.first()
    if team:
        athlete_data = {
            'name': '测试员',
            'gender': '男',
            'birth_date': '2000-01-01',
            'bay_area_hukou': '广东',
            'team': team.id,
        }
        athlete_serializer = AthleteSerializer(data=athlete_data)
        if athlete_serializer.is_valid():
            test_athlete = athlete_serializer.save()
            print(f"  ✓ 运动员创建成功: {test_athlete.name}")
            test_athlete.delete()
            print("  ✓ 测试数据已删除")
        else:
            print(f"  ✗ 运动员创建失败: {athlete_serializer.errors}")
    
except Exception as e:
    print(f"  ✗ 测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("验证完成！")
print("=" * 80)

