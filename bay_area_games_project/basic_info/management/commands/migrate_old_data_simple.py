"""
简单直接的数据迁移：从旧表复制到Django表
"""
import sqlite3
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
from basic_info.models import Team, Athlete


class Command(BaseCommand):
    help = "将旧表数据迁移到Django表（使用ORM）"

    def handle(self, *args, **options):
        db_path = settings.DATABASES['default']['NAME']
        if not hasattr(db_path, 'startswith'):  # 可能是Path对象
            db_path = str(db_path)
        if not db_path.startswith('/') and ':' not in db_path[:2]:
            db_path = str(settings.BASE_DIR / db_path)
        else:
            db_path = str(db_path)
        
        # 关闭Django连接
        connection.close()
        
        # 只读连接读取旧数据
        read_conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
        read_cursor = read_conn.cursor()
        
        try:
            # 1. 迁移 team
            self.stdout.write('正在迁移 team 数据...')
            read_cursor.execute('SELECT * FROM "team"')
            team_rows = read_cursor.fetchall()
            read_cursor.execute('PRAGMA table_info("team")')
            team_cols = [col[1] for col in read_cursor.fetchall()]
            
            Team.objects.all().delete()
            
            for row in team_rows:
                data = dict(zip(team_cols, row))
                # 移除主键
                if 'team_id' in data:
                    del data['team_id']
                
                # 确保必填字段存在
                if 'city_code' not in data or not data.get('city_code'):
                    # 从region生成city_code
                    region = data.get('region', '')
                    city_code_map = {'广州': '01', '香港': '03', '澳门': '04', '深圳': '02'}
                    data['city_code'] = city_code_map.get(region, '00')
                
                # 只保留Django模型中存在的字段
                team_data = {}
                for field in Team._meta.get_fields():
                    if hasattr(field, 'column') and field.column in data:
                        value = data[field.column]
                        if value is not None:
                            team_data[field.name] = value
                
                try:
                    Team.objects.create(**team_data)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  跳过team记录: {e}'))
            
            self.stdout.write(self.style.SUCCESS(f'  ✓ 已迁移 {Team.objects.count()} 条 team 记录'))
            
            # 2. 迁移 athlete
            self.stdout.write('正在迁移 athlete 数据...')
            read_cursor.execute('SELECT * FROM "athlete"')
            athlete_rows = read_cursor.fetchall()
            read_cursor.execute('PRAGMA table_info("athlete")')
            athlete_cols = [col[1] for col in read_cursor.fetchall()]
            
            # 建立team_id映射
            read_cursor.execute('SELECT team_id FROM "team" ORDER BY team_id')
            old_team_ids = [str(row[0]) for row in read_cursor.fetchall()]
            new_teams = list(Team.objects.all().order_by('id'))
            team_id_map = {}
            for i, old_id in enumerate(old_team_ids):
                if i < len(new_teams):
                    team_id_map[old_id] = new_teams[i]
            
            Athlete.objects.all().delete()
            
            for row in athlete_rows:
                data = dict(zip(athlete_cols, row))
                # 移除主键
                if 'athlete_id' in data:
                    del data['athlete_id']
                
                # 映射team_id
                if 'team_id' in data and data['team_id']:
                    old_team_id = str(data['team_id'])
                    if old_team_id in team_id_map:
                        data['team'] = team_id_map[old_team_id]
                    elif new_teams:
                        data['team'] = new_teams[0]
                    else:
                        continue
                    del data['team_id']
                
                # 只保留Django模型中存在的字段
                athlete_data = {}
                for field in Athlete._meta.get_fields():
                    if hasattr(field, 'column') and field.column in data:
                        value = data[field.column]
                        if value is not None:
                            athlete_data[field.name] = value
                    elif field.name in data:  # 可能字段名不同
                        value = data[field.name]
                        if value is not None:
                            athlete_data[field.name] = value
                
                try:
                    Athlete.objects.create(**athlete_data)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'  跳过athlete记录: {e}'))
            
            self.stdout.write(self.style.SUCCESS(f'  ✓ 已迁移 {Athlete.objects.count()} 条 athlete 记录'))
            
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS('数据迁移完成！'))
            self.stdout.write('='*50)
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'迁移失败: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())
        finally:
            read_conn.close()

