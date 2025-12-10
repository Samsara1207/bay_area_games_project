"""
直接测试API，查看详细错误
"""
import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from basic_info.models import Team, Athlete
from basic_info.serializers import TeamSerializer, AthleteSerializer

print("=" * 80)
print("测试API序列化")
print("=" * 80)

try:
    print("\n【测试Team】")
    teams = Team.objects.all()
    print(f"  查询到 {teams.count()} 个代表队")
    
    for team in teams[:3]:
        try:
            serializer = TeamSerializer(team)
            data = serializer.data
            print(f"  ✓ {team.team_name}: {len(data)} 字段")
        except Exception as e:
            print(f"  ✗ {team.team_name}: {e}")
            traceback.print_exc()
    
    print("\n【测试Athlete】")
    athletes = Athlete.objects.all()
    print(f"  查询到 {athletes.count()} 个运动员")
    
    for athlete in athletes[:3]:
        try:
            serializer = AthleteSerializer(athlete)
            data = serializer.data
            print(f"  ✓ {athlete.name}: {len(data)} 字段")
        except Exception as e:
            print(f"  ✗ {athlete.name}: {e}")
            traceback.print_exc()
            
except Exception as e:
    print(f"\n错误: {e}")
    traceback.print_exc()

