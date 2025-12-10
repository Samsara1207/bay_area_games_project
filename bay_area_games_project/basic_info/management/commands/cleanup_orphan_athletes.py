from django.core.management.base import BaseCommand
from basic_info.models import Athlete


class Command(BaseCommand):
    help = "删除 team 为 null 的孤儿运动员（会级联删除相关报名与成绩）"

    def handle(self, *args, **options):
        qs = Athlete.objects.filter(team__isnull=True)
        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS("没有孤儿运动员需要删除。"))
            return
        self.stdout.write(f"将删除 {total} 个孤儿运动员（及其相关数据）。")
        qs.delete()
        self.stdout.write(self.style.SUCCESS("删除完成。"))
