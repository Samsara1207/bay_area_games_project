"""
直接从备份数据库文件恢复（替换当前数据库）
"""
import os
import shutil
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = "直接从备份数据库文件恢复（会替换当前数据库文件）"

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='bay_area_games.db',
            help='源数据库文件路径（默认: bay_area_games.db）',
        )
        parser.add_argument(
            '--backup-current',
            action='store_true',
            help='恢复前备份当前数据库',
        )

    def handle(self, *args, **options):
        source_db = options.get('source', 'bay_area_games.db')
        backup_current = options.get('backup_current', False)
        
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
        target_db = str(target_db)  # 确保是字符串
        source_db = str(source_db)  # 确保是字符串
        
        self.stdout.write(f'源数据库: {source_db}')
        self.stdout.write(f'目标数据库: {target_db}')
        
        # 关闭 Django 的数据库连接
        connection.close()
        
        try:
            # 备份当前数据库
            if backup_current and os.path.exists(target_db):
                backup_path = str(target_db) + '.backup'
                shutil.copy2(target_db, backup_path)
                self.stdout.write(self.style.SUCCESS(f'已备份当前数据库到: {backup_path}'))
            
            # 直接复制数据库文件
            if os.path.exists(target_db):
                os.remove(target_db)
            
            shutil.copy2(source_db, target_db)
            self.stdout.write(self.style.SUCCESS('数据库文件已复制'))
            
            # 运行迁移确保结构一致（如果需要）
            self.stdout.write('正在检查数据库结构...')
            try:
                call_command('migrate', verbosity=0, interactive=False)
                self.stdout.write(self.style.SUCCESS('数据库结构已更新'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'迁移检查完成（可能无需更新）: {e}'))
            
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS('数据库恢复完成！'))
            self.stdout.write('='*50)
            self.stdout.write('\n注意：')
            self.stdout.write('1. 如果表结构有变化，可能需要运行: python manage.py migrate')
            self.stdout.write('2. 如果遇到问题，可以使用备份文件恢复')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'恢复过程中出错: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())

