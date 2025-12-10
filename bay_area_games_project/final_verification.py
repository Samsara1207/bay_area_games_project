"""
最终验证：确保所有功能正常
"""
import sqlite3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from django.db.models import Count
from basic_info.models import Team, Athlete
from result_management.models import Result, MedalHonor
from result_management.serializers import ResultSerializer, MedalHonorSerializer

print("=" * 80)
print("最终验证")
print("=" * 80)

# 1. 检查数据数量
print("\n【数据统计】")
print(f"  代表队: {Team.objects.count()}")
print(f"  运动员: {Athlete.objects.count()}")
print(f"  成绩: {Result.objects.count()}")
print(f"  奖牌: {MedalHonor.objects.count()}")

# 2. 检查重复的代表队
print("\n【检查重复数据】")
teams = Team.objects.values('team_name').annotate(count=Count('id')).filter(count__gt=1)
if teams:
    print(f"  ✗ 仍有重复的代表队: {list(teams)}")
else:
    print("  ✓ 无重复的代表队")

# 3. 测试序列化
print("\n【测试序列化】")
try:
    result = Result.objects.first()
    if result:
        serializer = ResultSerializer(result)
        print(f"  ✓ Result序列化成功: {len(serializer.data)} 字段")
    else:
        print("  ⚠ 无成绩数据")
except Exception as e:
    print(f"  ✗ Result序列化失败: {e}")

try:
    medal = MedalHonor.objects.first()
    if medal:
        serializer = MedalHonorSerializer(medal)
        print(f"  ✓ MedalHonor序列化成功: {len(serializer.data)} 字段")
    else:
        print("  ⚠ 无奖牌数据")
except Exception as e:
    print(f"  ✗ MedalHonor序列化失败: {e}")

# 4. 检查athlete表字段
print("\n【检查athlete表字段】")
from django.db import connection
cursor = connection.cursor()
cursor.execute('PRAGMA table_info("basic_info_athlete")')
cols = [col[1] for col in cursor.fetchall()]
required_fields = ['birth_date', 'bay_area_hukou', 'height', 'weight', 'qualification_status']
missing = [f for f in required_fields if f not in cols]
if missing:
    print(f"  ✗ 缺失字段: {missing}")
else:
    print("  ✓ 所有必需字段都存在")

print("\n" + "=" * 80)
print("验证完成！")
print("=" * 80)

