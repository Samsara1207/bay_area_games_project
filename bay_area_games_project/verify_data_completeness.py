"""
验证数据完整性：对比bay_area_games.db和db.sqlite3
"""
import sqlite3

source_db = 'bay_area_games.db'
target_db = 'db.sqlite3'

print("=" * 70)
print("数据完整性验证")
print("=" * 70)

source_conn = sqlite3.connect(source_db)
target_conn = sqlite3.connect(target_db)

source_cursor = source_conn.cursor()
target_cursor = target_conn.cursor()

# 表名映射
table_mapping = {
    'team': 'basic_info_team',
    'athlete': 'basic_info_athlete',
    'venue': 'event_management_venue',
    'event': 'event_management_event',
    'group': 'event_management_group',
    'athlete_event': 'event_management_athleteevent',
    'result': 'result_management_result',
    'medal_honor': 'result_management_medalhonor',
    'data_report': 'data_statistics_datareport',
    'referee': 'referee_management_referee',
    'referee_group': 'referee_management_refereegroup',
    'referee_arrangement': 'referee_management_refereearrangement',
    'supplier': 'logistics_supplier',
    'logistics_detail': 'logistics_logisticsdetail',
    'volunteer': 'logistics_volunteer',
    'schedule': 'operation_schedule',
    'event_operation': 'operation_eventoperation',
    'appeal': 'appeal_arbitration_appeal',
    'arbitration_committee': 'appeal_arbitration_arbitrationcommittee',
    'appeal_arbitration': 'appeal_arbitration_appealarbitration',
    'sponsor': 'business_sponsor',
    'sponsor_rights': 'business_sponsorrights',
    'audience_ticket': 'business_audienceticket',
    'finance': 'finance_safety_finance',
    'epidemic_safety': 'finance_safety_epidemicsafety',
}

print(f"\n{'源表':<30} {'源数据':<10} {'目标表':<35} {'目标数据':<10} {'状态'}")
print("-" * 70)

total_source = 0
total_target = 0
all_match = True

for old_table, django_table in table_mapping.items():
    try:
        # 源表数据
        source_cursor.execute(f'SELECT COUNT(*) FROM "{old_table}"')
        source_count = source_cursor.fetchone()[0]
        total_source += source_count
        
        # 目标表数据
        target_cursor.execute(f'SELECT COUNT(*) FROM "{django_table}"')
        target_count = target_cursor.fetchone()[0]
        total_target += target_count
        
        status = "✓" if source_count == target_count else "✗"
        if source_count != target_count:
            all_match = False
        
        print(f"{old_table:<30} {source_count:<10} {django_table:<35} {target_count:<10} {status}")
        
    except Exception as e:
        print(f"{old_table:<30} {'错误':<10} {django_table:<35} {'-':<10} ✗ ({str(e)[:30]})")
        all_match = False

print("-" * 70)
print(f"{'总计':<30} {total_source:<10} {'':<35} {total_target:<10} {'✓' if all_match else '✗'}")

source_conn.close()
target_conn.close()

print("\n" + "=" * 70)
if all_match:
    print("✓ 所有数据已完整迁移！")
else:
    print("✗ 部分数据不匹配，需要检查")
print("=" * 70)

