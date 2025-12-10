"""
从备份数据库文件复制数据到当前数据库（支持ID映射和外键处理）
"""
import os
import sqlite3
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = "从备份数据库文件复制所有数据（自动处理ID映射和外键关系）"

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='bay_area_games.db',
            help='源数据库文件路径（默认: bay_area_games.db）',
        )
        parser.add_argument(
            '--clear-first',
            action='store_true',
            help='复制前先清空目标数据库',
        )

    def handle(self, *args, **options):
        source_db = options.get('source', 'bay_area_games.db')
        clear_first = options.get('clear_first', False)
        
        # 检查源文件是否存在
        if not os.path.isabs(source_db):
            source_db = os.path.join(settings.BASE_DIR, source_db)
        
        if not os.path.exists(source_db):
            self.stdout.write(self.style.ERROR(f'源数据库文件不存在: {source_db}'))
            return
        
        # 获取目标数据库路径
        target_db = settings.DATABASES['default']['NAME']
        if not os.path.isabs(target_db):
            target_db = os.path.join(settings.BASE_DIR, target_db)
        
        self.stdout.write(f'源数据库: {source_db}')
        self.stdout.write(f'目标数据库: {target_db}')
        
        # 关闭 Django 的数据库连接
        connection.close()
        
        try:
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
                'referee': 'referee_management_referee',
                'referee_group': 'referee_management_refereegroup',
                'referee_arrangement': 'referee_management_refereearrangement',
                'result': 'result_management_result',
                'medal_honor': 'result_management_medalhonor',
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
                'data_report': 'data_statistics_datareport',
            }
            
            # 复制顺序（先复制无外键依赖的表）
            copy_order = [
                'venue', 'supplier', 'volunteer', 'sponsor',  # 无外键
                'team',  # 基础表
                'referee',  # 基础表
                'arbitration_committee',  # 基础表
                'event',  # 依赖 venue, referee_group
                'group',  # 依赖 event
                'referee_group',  # 依赖 referee, event
                'athlete',  # 依赖 team
                'athlete_event',  # 依赖 athlete, event, group
                'result',  # 依赖 athlete_event
                'medal_honor',  # 依赖 result, athlete, team
                'appeal',  # 依赖 athlete, event
                'appeal_arbitration',  # 依赖 appeal, arbitration_committee
                'referee_arrangement',  # 依赖 referee_group, referee, event
                'schedule',  # 依赖 event, venue
                'event_operation',  # 依赖 event
                'sponsor_rights',  # 依赖 sponsor, event, finance
                'audience_ticket',  # 依赖 event
                'logistics_detail',  # 依赖 supplier
                'finance',  # 可能被 sponsor_rights 引用
                'epidemic_safety',  # 无外键（person_id 是通用ID）
                'data_report',  # 无外键
            ]
            
            if clear_first:
                self.stdout.write(self.style.WARNING('正在清空目标数据库...'))
                target_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                tables = [row[0] for row in target_cursor.fetchall()]
                target_cursor.execute("PRAGMA foreign_keys = OFF")
                for table in tables:
                    target_cursor.execute(f'DELETE FROM "{table}"')
                target_cursor.execute("PRAGMA foreign_keys = ON")
                target_conn.commit()
                self.stdout.write(self.style.SUCCESS('目标数据库已清空'))
            
            # ID映射字典：{表名: {源ID: 目标ID}}
            id_mappings = {}
            copied_count = 0
            
            self.stdout.write('\n开始分阶段复制数据...\n')
            
            target_cursor.execute("PRAGMA foreign_keys = OFF")
            
            for table in copy_order:
                if table not in table_mapping:
                    continue
                
                target_table = table_mapping[table]
                
                # 检查目标表是否存在
                target_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{target_table}'")
                if not target_cursor.fetchone():
                    self.stdout.write(self.style.WARNING(f'  跳过 {table}（目标表不存在）'))
                    continue
                
                try:
                    # 获取列信息
                    source_cursor.execute(f'PRAGMA table_info("{table}")')
                    source_cols = {col[1]: col for col in source_cursor.fetchall()}
                    
                    target_cursor.execute(f'PRAGMA table_info("{target_table}")')
                    target_cols = {col[1]: col for col in target_cursor.fetchall()}
                    
                    # 构建列映射
                    source_select = []
                    target_insert = []
                    id_mapping_key = None
                    
                    for source_col_name, source_col_info in source_cols.items():
                        # 跳过源表的主键（xxx_id）
                        if source_col_name.endswith('_id') and source_col_name != 'id' and source_col_name.replace('_id', '') == table.split('_')[-1]:
                            # 这是主键，需要映射
                            if 'id' in target_cols:
                                id_mapping_key = source_col_name
                                continue
                        
                        # 处理外键列
                        if source_col_name.endswith('_id') and source_col_name in target_cols:
                            source_select.append(f'"{source_col_name}"')
                            target_insert.append(f'"{source_col_name}"')
                        elif source_col_name in target_cols:
                            source_select.append(f'"{source_col_name}"')
                            target_insert.append(f'"{source_col_name}"')
                    
                    if not source_select:
                        continue
                    
                    # 查询源数据
                    select_sql = f'SELECT {",".join(source_select)} FROM "{table}"'
                    source_cursor.execute(select_sql)
                    rows = source_cursor.fetchall()
                    
                    if not rows:
                        continue
                    
                    # 插入数据
                    placeholders = ','.join(['?' for _ in target_insert])
                    insert_cols = ','.join(target_insert)
                    insert_sql = f'INSERT INTO "{target_table}" ({insert_cols}) VALUES ({placeholders})'
                    
                    # 处理ID映射和外键转换
                    processed_rows = []
                    table_id_map = {}
                    
                    for row in rows:
                        processed_row = list(row)
                        
                        # 如果有主键映射，记录并生成新ID
                        if id_mapping_key:
                            source_id = None
                            # 从源数据中找到主键值（需要重新查询）
                            source_cursor.execute(f'SELECT "{id_mapping_key}" FROM "{table}" LIMIT 1 OFFSET {len(processed_rows)}')
                            pk_result = source_cursor.fetchone()
                            if pk_result:
                                source_id = pk_result[0]
                        
                        # 转换外键ID
                        for i, col_name in enumerate([s.replace('"', '') for s in source_select]):
                            if col_name.endswith('_id') and col_name != 'id':
                                # 这是外键，需要映射
                                fk_table = col_name.replace('_id', '')
                                if fk_table in id_mappings:
                                    # 查找映射的ID
                                    source_fk_id = processed_row[i]
                                    if source_fk_id and str(source_fk_id) in id_mappings[fk_table]:
                                        processed_row[i] = id_mappings[fk_table][str(source_fk_id)]
                                    elif source_fk_id:
                                        # 如果找不到映射，尝试直接转换
                                        try:
                                            processed_row[i] = int(source_fk_id) if str(source_fk_id).isdigit() else None
                                        except:
                                            processed_row[i] = None
                            
                            # 数据类型转换
                            if isinstance(processed_row[i], str) and processed_row[i].isdigit():
                                try:
                                    processed_row[i] = int(processed_row[i])
                                except:
                                    pass
                        
                        processed_rows.append(tuple(processed_row))
                        
                        # 记录ID映射
                        if id_mapping_key:
                            # 获取插入后的自增ID
                            target_cursor.execute(insert_sql, tuple(processed_row))
                            new_id = target_cursor.lastrowid
                            if source_id:
                                if table not in id_mappings:
                                    id_mappings[table] = {}
                                id_mappings[table][str(source_id)] = new_id
                        else:
                            target_cursor.execute(insert_sql, tuple(processed_row))
                    
                    target_conn.commit()
                    
                    table_display = f'{table} -> {target_table}'
                    self.stdout.write(self.style.SUCCESS(f'  ✓ {table_display}: {len(rows)} 条记录'))
                    copied_count += len(rows)
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ {table}: {str(e)[:100]}'))
                    target_conn.rollback()
            
            target_cursor.execute("PRAGMA foreign_keys = ON")
            source_conn.close()
            target_conn.close()
            
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS(f'复制完成！共复制 {copied_count} 条记录'))
            self.stdout.write('='*50)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'复制过程中出错: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

