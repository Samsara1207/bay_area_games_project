"""
从备份数据库文件复制数据到当前数据库
"""
import os
import sqlite3
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = "从备份数据库文件（如 bay_area_games.db）复制所有数据到当前数据库"

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
            self.stdout.write(self.style.WARNING('请确保 bay_area_games.db 文件在项目根目录下'))
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
            # 连接源数据库和目标数据库
            source_conn = sqlite3.connect(source_db)
            target_conn = sqlite3.connect(target_db)
            
            source_cursor = source_conn.cursor()
            target_cursor = target_conn.cursor()
            
            # 如果指定清空，先清空目标数据库
            if clear_first:
                self.stdout.write(self.style.WARNING('正在清空目标数据库...'))
                target_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
                tables = [row[0] for row in target_cursor.fetchall()]
                
                target_cursor.execute("PRAGMA foreign_keys = OFF")
                for table in tables:
                    target_cursor.execute(f"DELETE FROM {table}")
                target_cursor.execute("PRAGMA foreign_keys = ON")
                target_conn.commit()
                self.stdout.write(self.style.SUCCESS('目标数据库已清空'))
            
            # 获取源数据库的所有表
            source_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            source_tables = [row[0] for row in source_cursor.fetchall()]
            
            self.stdout.write(f'\n找到 {len(source_tables)} 个表，开始复制数据...')
            
            # 禁用外键检查
            target_cursor.execute("PRAGMA foreign_keys = OFF")
            
            copied_count = 0
            error_count = 0
            
            # 表名映射：源数据库表名 -> 目标数据库表名
            table_mapping = {
                'team': 'basic_info_team',
                'athlete': 'basic_info_athlete',
                'venue': 'event_management_venue',
                'event': 'event_management_event',
                'group': 'event_management_group',  # group 是 SQL 关键字
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
            
            for table in source_tables:
                try:
                    # 确定目标表名
                    target_table = table_mapping.get(table, table)
                    
                    # 检查目标表是否存在
                    target_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{target_table}'")
                    if not target_cursor.fetchone():
                        # 如果映射的表不存在，尝试使用原表名
                        target_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                        if not target_cursor.fetchone():
                            self.stdout.write(self.style.WARNING(f'  跳过表 {table}（目标数据库中不存在）'))
                            continue
                        target_table = table
                    
                    # 获取源表结构
                    source_cursor.execute(f'PRAGMA table_info("{table}")')
                    source_columns = {col[1]: col for col in source_cursor.fetchall()}
                    
                    # 获取目标表结构
                    target_cursor.execute(f'PRAGMA table_info("{target_table}")')
                    target_columns = {col[1]: col for col in target_cursor.fetchall()}
                    
                    if not source_columns or not target_columns:
                        continue
                    
                    # 构建列名映射：源列名 -> 目标列名
                    # 规则：xxx_id -> id（主键），其他列名保持不变
                    column_mapping = {}
                    source_col_list = []
                    target_col_list = []
                    
                    for source_col_name in source_columns.keys():
                        # 主键映射：team_id -> id, athlete_id -> id 等
                        if source_col_name.endswith('_id') and source_col_name != 'id':
                            # 检查是否是主键（通常是第一个列或名为 xxx_id）
                            if 'id' in target_columns:
                                # 跳过源的主键列，使用目标的自增ID
                                continue
                        elif source_col_name == 'id' and 'id' in target_columns:
                            # 如果源表也有 id 列，直接映射
                            column_mapping[source_col_name] = 'id'
                            source_col_list.append(source_col_name)
                            target_col_list.append('id')
                        elif source_col_name in target_columns:
                            # 列名相同，直接映射
                            column_mapping[source_col_name] = source_col_name
                            source_col_list.append(source_col_name)
                            target_col_list.append(source_col_name)
                        # 其他列忽略（目标表中不存在）
                    
                    if not source_col_list:
                        self.stdout.write(self.style.WARNING(f'  跳过表 {table}（无匹配列）'))
                        continue
                    
                    # 清空目标表
                    target_cursor.execute(f'DELETE FROM "{target_table}"')
                    
                    # 复制数据（只选择匹配的列）
                    source_cols_str = ','.join([f'"{col}"' for col in source_col_list])
                    source_cursor.execute(f'SELECT {source_cols_str} FROM "{table}"')
                    rows = source_cursor.fetchall()
                    
                    if rows:
                        # 构建 INSERT 语句
                        placeholders = ','.join(['?' for _ in target_col_list])
                        target_cols_str = ','.join([f'"{col}"' for col in target_col_list])
                        insert_sql = f'INSERT INTO "{target_table}" ({target_cols_str}) VALUES ({placeholders})'
                        
                        # 处理数据类型转换（TEXT ID -> INTEGER ID）
                        processed_rows = []
                        for row in rows:
                            processed_row = []
                            for i, val in enumerate(row):
                                source_col = source_col_list[i]
                                target_col = target_col_list[i]
                                
                                # 如果是ID列且源是TEXT类型，尝试转换为INTEGER
                                if target_col == 'id' or (target_col.endswith('_id') and source_col.endswith('_id')):
                                    try:
                                        if val is not None and isinstance(val, str):
                                            # 尝试转换为整数
                                            val = int(val) if val.isdigit() else None
                                    except:
                                        pass
                                
                                processed_row.append(val)
                            processed_rows.append(tuple(processed_row))
                        
                        target_cursor.executemany(insert_sql, processed_rows)
                        target_conn.commit()
                        
                        table_display = f'{table}' + (f' -> {target_table}' if table != target_table else '')
                        self.stdout.write(self.style.SUCCESS(f'  ✓ {table_display}: {len(rows)} 条记录'))
                        copied_count += len(rows)
                    else:
                        self.stdout.write(f'  - {table}: 无数据')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ {table}: 复制失败 - {e}'))
                    error_count += 1
                    target_conn.rollback()
            
            # 重新启用外键检查
            target_cursor.execute("PRAGMA foreign_keys = ON")
            
            # 复制 sqlite_sequence（自增ID序列）
            try:
                source_cursor.execute("SELECT name, seq FROM sqlite_sequence")
                sequences = source_cursor.fetchall()
                if sequences:
                    target_cursor.execute("DELETE FROM sqlite_sequence")
                    target_cursor.executemany("INSERT INTO sqlite_sequence (name, seq) VALUES (?, ?)", sequences)
                    target_conn.commit()
                    self.stdout.write(self.style.SUCCESS(f'  已复制 {len(sequences)} 个自增序列'))
            except:
                pass  # 如果没有 sqlite_sequence 表，忽略
            
            source_conn.close()
            target_conn.close()
            
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS(f'复制完成！'))
            self.stdout.write(f'  成功复制: {copied_count} 条记录')
            if error_count > 0:
                self.stdout.write(self.style.WARNING(f'  失败: {error_count} 个表'))
            self.stdout.write('='*50)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'复制过程中出错: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

