"""
修复运动员资格状态：
1. 已参赛的运动员（有athlete_event记录）自动审核通过
2. 创建更多有差异性的测试运动员
"""
import sqlite3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bay_area_games.settings')
django.setup()

from django.conf import settings
from basic_info.models import Athlete
from event_management.models import AthleteEvent

db_path = settings.DATABASES['default']['NAME']
if not os.path.isabs(db_path):
    db_path = str(settings.BASE_DIR / db_path)
else:
    db_path = str(db_path)

print("=" * 80)
print("修复运动员资格状态")
print("=" * 80)

# 1. 已参赛的运动员自动审核通过
print("\n【1. 已参赛运动员自动审核通过】")
athletes_with_events = Athlete.objects.filter(
    id__in=AthleteEvent.objects.values_list('athlete_id', flat=True)
).exclude(qualification_status='已审核')

updated = 0
for athlete in athletes_with_events:
    athlete.qualification_status = '已审核'
    athlete.save(update_fields=['qualification_status'])
    updated += 1
    print(f"  ✓ {athlete.name}: 已审核通过")

print(f"\n  ✓ 共更新 {updated} 条记录")

# 2. 创建更多有差异性的测试运动员
print("\n【2. 创建有差异性的测试运动员】")
from datetime import date, timedelta
import random

teams = list(Athlete.objects.values_list('team_id', flat=True).distinct())
if not teams:
    from basic_info.models import Team
    teams = list(Team.objects.values_list('id', flat=True))

if teams:
    test_athletes = [
        {
            'name': '张强',
            'gender': '男',
            'birth_date': date(1995, 3, 15),
            'bay_area_hukou': '广东',
            'height': 1.85,
            'weight': 80.0,
            'qualification_status': '已审核',
            'doping_test': '合格',
            'team_id': teams[0] if teams else None,
        },
        {
            'name': '王美丽',
            'gender': '女',
            'birth_date': date(1998, 7, 22),
            'bay_area_hukou': '香港',
            'height': 1.70,
            'weight': 60.0,
            'qualification_status': '未审核',
            'doping_test': '待检测',
            'team_id': teams[1] if len(teams) > 1 else teams[0],
        },
        {
            'name': '李志明',
            'gender': '男',
            'birth_date': date(2000, 11, 8),
            'bay_area_hukou': '澳门',
            'height': 1.75,
            'weight': 70.0,
            'qualification_status': '已审核',
            'doping_test': '合格',
            'team_id': teams[2] if len(teams) > 2 else teams[0],
        },
        {
            'name': '陈小芳',
            'gender': '女',
            'birth_date': date(1997, 5, 30),
            'bay_area_hukou': '广东',
            'height': 1.68,
            'weight': 55.0,
            'qualification_status': '驳回',
            'doping_test': '不合格',
            'team_id': teams[0] if teams else None,
        },
    ]
    
    created = 0
    for athlete_data in test_athletes:
        if athlete_data['team_id']:
            # 检查是否已存在
            if not Athlete.objects.filter(name=athlete_data['name']).exists():
                athlete_data['id_card'] = ''
                athlete_data['phone'] = ''
                Athlete.objects.create(**athlete_data)
                created += 1
                print(f"  ✓ 创建: {athlete_data['name']} ({athlete_data['gender']}, {athlete_data['qualification_status']})")
    
    print(f"\n  ✓ 共创建 {created} 个测试运动员")
else:
    print("  ⚠ 没有可用的代表队，跳过创建测试运动员")

print("\n" + "=" * 80)
print("修复完成！")
print("=" * 80)

