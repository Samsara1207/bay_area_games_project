"""
将旧表（team, athlete）的数据迁移到新表（basic_info_team, basic_info_athlete）
"""
import os
import sqlite3
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from basic_info.models import Team, Athlete


class Command(BaseCommand):
    help = "将旧表数据迁移到Django表"

    def handle(self, *args, **options):
        db_path = settings.DATABASES['default']['NAME']
        if not os.path.isabs(db_path):
            db_path = str(settings.BASE_DIR / db_path)
        else:
            db_path = str(db_path)
        
        # 使用Django的数据库连接
        from django.db import connections
        db_conn = connections['default']
        
        # 使用原始SQL
        with db_conn.cursor() as cursor:
            try:
                # 1. 迁移 team 表数据
                self.stdout.write('正在迁移 team 表数据...')
                cursor.execute('SELECT COUNT(*) FROM "team"')
                team_count = cursor.fetchone()[0]
                
                # 临时连接只读数据库读取旧数据
                read_conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
                read_cursor = read_conn.cursor()
                
                if team_count > 0:
                    # 获取列名（排除主键）
                    read_cursor.execute('PRAGMA table_info("team")')
                    team_cols = [col[1] for col in read_cursor.fetchall() if col[1] != 'team_id']
                    
                    cursor.execute('PRAGMA table_info("basic_info_team")')
                    new_team_cols = [col[1] for col in cursor.fetchall() if col[1] != 'id']
                    
                    # 找到共同列
                    common_cols = [col for col in team_cols if col in new_team_cols]
                    
                    if common_cols:
                        # 清空新表
                        cursor.execute('DELETE FROM "basic_info_team"')
                        
                    # 检查目标表是否有必填字段但源表没有
                    cursor.execute('PRAGMA table_info("basic_info_team")')
                    target_all_cols = {col[1]: col for col in cursor.fetchall()}
                    
                    # 添加缺失的必填字段（使用默认值）
                    for col_name, col_info in target_all_cols.items():
                        if col_name not in common_cols and col_name != 'id' and col_info[3] == 1:  # NOT NULL
                            if col_name == 'city_code':
                                # 如果没有city_code，使用region的前两个字符
                                common_cols.append('city_code')
                                # 需要从region生成city_code
                    
                    # 复制数据（只复制共同列）
                    select_cols = ','.join([f'"{col}"' for col in common_cols if col != 'city_code'])
                    insert_cols = ','.join([f'"{col}"' for col in common_cols])
                    
                    # 从只读连接读取
                    read_cursor.execute(f'SELECT {select_cols} FROM "team"')
                    rows = read_cursor.fetchall()
                    
                    # 处理每一行，添加缺失字段
                    processed_rows = []
                    for row in rows:
                        row_list = list(row)
                        # 如果缺少city_code，从region生成
                        if 'city_code' in common_cols and 'city_code' not in select_cols:
                            # 需要获取region值
                            row_dict = dict(zip([c for c in common_cols if c != 'city_code'], row_list))
                            if 'region' in row_dict:
                                region = row_dict.get('region', '')
                                # 简单的映射
                                city_code_map = {'广州': '01', '香港': '03', '澳门': '04'}
                                city_code = city_code_map.get(region, '00')
                                # 在region之后插入city_code
                                region_idx = [c for c in common_cols if c != 'city_code'].index('region') if 'region' in [c for c in common_cols if c != 'city_code'] else -1
                                if region_idx >= 0:
                                    row_list.insert(region_idx + 1, city_code)
                                else:
                                    row_list.append(city_code)
                        processed_rows.append(tuple(row_list))
                    
                    placeholders = ','.join(['?' for _ in common_cols])
                    for row in processed_rows:
                        cursor.execute(f'INSERT INTO "basic_info_team" ({insert_cols}) VALUES ({placeholders})', row)
                        
                        cursor.execute('SELECT COUNT(*) FROM "basic_info_team"')
                        new_count = cursor.fetchone()[0]
                        
                        self.stdout.write(self.style.SUCCESS(f'  ✓ team: {team_count} -> basic_info_team: {new_count} 条记录'))
                    else:
                        self.stdout.write(self.style.WARNING('  team 表无匹配列'))
                else:
                    self.stdout.write('  team 表无数据')
                
                # 2. 迁移 athlete 表数据
                self.stdout.write('正在迁移 athlete 表数据...')
                read_cursor.execute('SELECT COUNT(*) FROM "athlete"')
                athlete_count = read_cursor.fetchone()[0]
                
                if athlete_count > 0:
                    # 获取列名
                    read_cursor.execute('PRAGMA table_info("athlete")')
                    athlete_cols = [col[1] for col in read_cursor.fetchall() if col[1] != 'athlete_id']
                    
                    cursor.execute('PRAGMA table_info("basic_info_athlete")')
                    new_athlete_cols = [col[1] for col in cursor.fetchall() if col[1] != 'id']
                    
                    # 找到共同列
                    common_cols = [col for col in athlete_cols if col in new_athlete_cols]
                    
                    if common_cols:
                        # 建立 team_id 映射（旧ID -> 新ID）
                        read_cursor.execute('SELECT team_id FROM "team" ORDER BY team_id')
                        old_team_ids = [str(row[0]) for row in read_cursor.fetchall()]
                        
                        cursor.execute('SELECT id FROM "basic_info_team" ORDER BY id')
                        new_team_ids = [row[0] for row in cursor.fetchall()]
                        
                        team_id_map = {}
                        for i, old_id in enumerate(old_team_ids):
                            if i < len(new_team_ids):
                                team_id_map[old_id] = new_team_ids[i]
                        
                        # 清空新表
                        cursor.execute('DELETE FROM "basic_info_athlete"')
                        
                        # 读取旧表数据
                        select_cols = ','.join([f'"{col}"' for col in common_cols])
                        read_cursor.execute(f'SELECT {select_cols} FROM "athlete"')
                        rows = read_cursor.fetchall()
                        
                        # 复制数据并映射team_id
                        insert_cols = ','.join([f'"{col}"' for col in common_cols])
                        placeholders = ','.join(['?' for _ in common_cols])
                        
                        for row in rows:
                            row_list = list(row)
                            row_dict = dict(zip(common_cols, row_list))
                            
                            # 映射 team_id
                            if 'team_id' in row_dict and row_dict['team_id']:
                                old_team_id = str(row_dict['team_id'])
                                if old_team_id in team_id_map:
                                    team_id_idx = common_cols.index('team_id')
                                    row_list[team_id_idx] = team_id_map[old_team_id]
                                elif new_team_ids:
                                    team_id_idx = common_cols.index('team_id')
                                    row_list[team_id_idx] = new_team_ids[0]
                                else:
                                    continue
                            
                            cursor.execute(f'INSERT INTO "basic_info_athlete" ({insert_cols}) VALUES ({placeholders})', tuple(row_list))
                        
                        cursor.execute('SELECT COUNT(*) FROM "basic_info_athlete"')
                        new_count = cursor.fetchone()[0]
                        
                        self.stdout.write(self.style.SUCCESS(f'  ✓ athlete: {athlete_count} -> basic_info_athlete: {new_count} 条记录'))
                    else:
                        self.stdout.write(self.style.WARNING('  athlete 表无匹配列'))
                else:
                    self.stdout.write('  athlete 表无数据')
                
                self.stdout.write('\n' + '='*50)
                self.stdout.write(self.style.SUCCESS('数据迁移完成！'))
                self.stdout.write('='*50)
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'迁移失败: {e}'))
                import traceback
                self.stdout.write(traceback.format_exc())
            finally:
                if 'read_conn' in locals():
                    read_conn.close()

