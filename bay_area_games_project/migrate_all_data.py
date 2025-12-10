"""
迁移所有表的数据从旧表到Django表
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

print(f"数据库路径: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 表名映射
table_mapping = {
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

# 只读连接读取旧数据
read_conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
read_cursor = read_conn.cursor()

total_migrated = 0

for old_table, django_table in table_mapping.items():
    try:
        # 检查表是否存在
        cursor.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{django_table}"')
        if not cursor.fetchone():
            print(f"跳过 {django_table}（表不存在）")
            continue
        
        # 检查旧表是否存在
        read_cursor.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{old_table}"')
        if not read_cursor.fetchone():
            print(f"跳过 {old_table}（源表不存在）")
            continue
        
        # 获取列信息
        read_cursor.execute(f'PRAGMA table_info("{old_table}")')
        old_cols = {col[1]: col for col in read_cursor.fetchall()}
        
        cursor.execute(f'PRAGMA table_info("{django_table}")')
        django_cols = {col[1]: col for col in cursor.fetchall()}
        
        # 找到共同列（排除主键）
        common_cols = []
        for col_name in old_cols.keys():
            if col_name.endswith('_id') and col_name.replace('_id', '') == old_table.split('_')[-1]:
                continue  # 跳过主键
            if col_name in django_cols and col_name != 'id':
                common_cols.append(col_name)
        
        if not common_cols:
            print(f"跳过 {old_table} -> {django_table}（无共同列）")
            continue
        
        # 清空Django表
        cursor.execute(f'DELETE FROM "{django_table}"')
        
        # 读取旧数据
        select_cols = ','.join([f'"{col}"' for col in common_cols])
        read_cursor.execute(f'SELECT {select_cols} FROM "{old_table}"')
        rows = read_cursor.fetchall()
        
        if not rows:
            print(f"  - {old_table} -> {django_table}: 无数据")
            continue
        
        # 插入数据
        insert_cols = ','.join([f'"{col}"' for col in common_cols])
        placeholders = ','.join(['?' for _ in common_cols])
        
        # 处理外键映射
        inserted_count = 0
        for row in rows:
            row_list = list(row)
            row_dict = dict(zip(common_cols, row_list))
            
            # 处理外键映射
            needs_mapping = False
            for col in common_cols:
                if col.endswith('_id') and col != 'id':
                    # 这是外键，可能需要映射
                    fk_table = col.replace('_id', '')
                    if fk_table in table_mapping:
                        # 需要映射
                        old_fk_id = row_dict[col]
                        if old_fk_id:
                            # 查找映射
                            read_cursor.execute(f'SELECT {fk_table}_id FROM "{fk_table}" ORDER BY {fk_table}_id')
                            old_ids = [str(r[0]) for r in read_cursor.fetchall()]
                            cursor.execute(f'SELECT id FROM "{table_mapping[fk_table]}" ORDER BY id')
                            new_ids = [r[0] for r in cursor.fetchall()]
                            
                            if str(old_fk_id) in old_ids:
                                idx = old_ids.index(str(old_fk_id))
                                if idx < len(new_ids):
                                    fk_idx = common_cols.index(col)
                                    row_list[fk_idx] = new_ids[idx]
                                    needs_mapping = True
            
            try:
                cursor.execute(f'INSERT INTO "{django_table}" ({insert_cols}) VALUES ({placeholders})', tuple(row_list))
                inserted_count += 1
            except Exception as e:
                # 如果插入失败，尝试处理缺失的必填字段
                if 'NOT NULL' in str(e):
                    # 跳过这条记录
                    continue
                else:
                    raise
        
        conn.commit()
        print(f"  ✓ {old_table} -> {django_table}: {inserted_count}/{len(rows)} 条记录")
        total_migrated += inserted_count
        
    except Exception as e:
        print(f"  ✗ {old_table} -> {django_table}: 错误 - {str(e)[:100]}")
        conn.rollback()

read_conn.close()
conn.close()

print("\n" + "="*60)
print(f"数据迁移完成！共迁移 {total_migrated} 条记录")
print("="*60)

