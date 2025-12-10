"""
重置数据库到初始状态
"""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "重置数据库到初始状态（清空所有数据并重新导入示例数据）"

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-structure',
            action='store_true',
            help='保留数据库结构，只清空数据（不删除数据库文件）',
        )

    def handle(self, *args, **options):
        keep_structure = options.get('keep_structure', False)
        
        if keep_structure:
            # 只清空数据，保留结构
            self.stdout.write(self.style.WARNING('正在清空所有数据...'))
            self.clear_all_data()
            self.stdout.write(self.style.SUCCESS('数据已清空'))
        else:
            # 完全重置：删除数据库文件并重新创建
            self.stdout.write(self.style.WARNING('正在重置数据库...'))
            self.reset_database_file()
        
        # 重新导入示例数据
        self.stdout.write(self.style.SUCCESS('正在导入示例数据...'))
        call_command('load_sample_data')
        self.stdout.write(self.style.SUCCESS('数据库已恢复到初始状态！'))

    def clear_all_data(self):
        """清空所有表的数据"""
        with connection.cursor() as cursor:
            # 获取所有表名
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # 禁用外键检查
            cursor.execute("PRAGMA foreign_keys = OFF")
            
            # 清空所有表
            for table in tables:
                try:
                    cursor.execute(f"DELETE FROM {table}")
                    self.stdout.write(f"  已清空表: {table}")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  清空表 {table} 失败: {e}"))
            
            # 重置自增ID
            for table in tables:
                try:
                    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
                except:
                    pass  # 如果表没有自增字段，会失败，忽略
            
            # 重新启用外键检查
            cursor.execute("PRAGMA foreign_keys = ON")

    def reset_database_file(self):
        """删除数据库文件并重新创建"""
        import os
        from django.conf import settings
        
        db_path = settings.DATABASES['default']['NAME']
        
        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(db_path):
            db_path = os.path.join(settings.BASE_DIR, db_path)
        
        if os.path.exists(db_path):
            try:
                # 关闭数据库连接
                connection.close()
                # 删除数据库文件
                os.remove(db_path)
                self.stdout.write(self.style.SUCCESS(f'已删除数据库文件: {db_path}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'删除数据库文件失败: {e}'))
                return
        
        # 重新创建数据库结构
        self.stdout.write('正在重新创建数据库结构...')
        call_command('migrate', verbosity=0)
        self.stdout.write(self.style.SUCCESS('数据库结构已创建'))

