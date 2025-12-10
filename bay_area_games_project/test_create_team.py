"""
测试创建代表队和运动员
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from basic_info.models import Team, Athlete
from basic_info.serializers import TeamSerializer, AthleteSerializer

print("=" * 80)
print("测试创建操作")
print("=" * 80)

# 测试创建代表队
print("\n【测试创建代表队】")
team_data = {
    'team_name': '测试代表队',
    'region': '深圳',
    'city_code': '02',
    'leader_name': '测试领队',
    'leader_phone': '13800000000',
    'team_code': 'SZ',
    'sport_type': '综合',
    'is_active': True,
}

try:
    serializer = TeamSerializer(data=team_data)
    if serializer.is_valid():
        team = serializer.save()
        print(f"  ✓ 创建成功: {team.team_name} (ID: {team.id})")
        # 删除测试数据
        team.delete()
        print("  ✓ 测试数据已删除")
    else:
        print(f"  ✗ 验证失败: {serializer.errors}")
except Exception as e:
    print(f"  ✗ 创建失败: {e}")
    import traceback
    traceback.print_exc()

# 测试创建运动员
print("\n【测试创建运动员】")
# 获取一个代表队
team = Team.objects.first()
if team:
    athlete_data = {
        'name': '测试运动员',
        'gender': '男',
        'birth_date': '2000-01-01',
        'bay_area_hukou': '广东',
        'doping_test': '待检测',
        'team': team.id,
    }
    
    try:
        serializer = AthleteSerializer(data=athlete_data)
        if serializer.is_valid():
            athlete = serializer.save()
            print(f"  ✓ 创建成功: {athlete.name} (ID: {athlete.id})")
            # 删除测试数据
            athlete.delete()
            print("  ✓ 测试数据已删除")
        else:
            print(f"  ✗ 验证失败: {serializer.errors}")
    except Exception as e:
        print(f"  ✗ 创建失败: {e}")
        import traceback
        traceback.print_exc()
else:
    print("  ✗ 没有可用的代表队")

