"""
裁判管理业务逻辑服务
"""
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta

from .models import Referee, RefereeArrangement, RefereeGroup


class RefereeService:
    """裁判服务类"""
    
    @staticmethod
    def get_referee_statistics():
        """获取裁判统计信息"""
        total = Referee.objects.count()
        by_level = Referee.objects.values('referee_level').annotate(
            count=Count('id')
        )
        bay_certified = Referee.objects.filter(bay_cert="有").count()
        
        return {
            "total": total,
            "by_level": list(by_level),
            "bay_certified": bay_certified,
        }
    
    @staticmethod
    def get_referee_workload(referee_id, start_date=None, end_date=None):
        """获取裁判工作量统计"""
        referee = Referee.objects.get(id=referee_id)
        arrangements = referee.arrangements.all()
        
        if start_date:
            arrangements = arrangements.filter(arrange_date__gte=start_date)
        if end_date:
            arrangements = arrangements.filter(arrange_date__lte=end_date)
        
        total = arrangements.count()
        checked_in = arrangements.filter(check_in_status="已签到").count()
        upcoming = arrangements.filter(
            arrange_date__gte=timezone.now(),
            check_in_status="未签到"
        ).count()
        
        return {
            "referee_name": referee.name,
            "total_arrangements": total,
            "checked_in": checked_in,
            "upcoming": upcoming,
            "attendance_rate": round(checked_in / total * 100, 2) if total > 0 else 0,
        }
    
    @staticmethod
    def check_referee_availability(referee_id, arrange_date):
        """检查裁判在指定时间是否可用"""
        referee = Referee.objects.get(id=referee_id)
        
        # 检查是否有时间冲突（同一时间段的执裁安排）
        conflict = RefereeArrangement.objects.filter(
            referee=referee,
            arrange_date=arrange_date,
            check_in_status__in=["已签到", "未签到"]
        ).exists()
        
        return not conflict


class RefereeGroupService:
    """裁判组服务类"""
    
    @staticmethod
    def create_group_with_referees(group_name, event_id, leader_referee_id=None, referee_ids=None):
        """创建裁判组并添加裁判"""
        from event_management.models import Event
        
        event = Event.objects.get(id=event_id)
        leader_referee = None
        if leader_referee_id:
            leader_referee = Referee.objects.get(id=leader_referee_id)
        
        group = RefereeGroup.objects.create(
            group_name=group_name,
            event=event,
            leader_referee=leader_referee,
        )
        
        if referee_ids:
            for referee_id in referee_ids:
                Referee.objects.get(id=referee_id)  # 验证存在
        
        return group
    
    @staticmethod
    def get_group_statistics(group_id):
        """获取裁判组统计信息"""
        group = RefereeGroup.objects.get(id=group_id)
        
        arrangements = group.arrangements.all()
        referee_count = arrangements.values('referee').distinct().count()
        total_arrangements = arrangements.count()
        checked_in = arrangements.filter(check_in_status="已签到").count()
        
        return {
            "group_name": group.group_name,
            "event_name": group.event.event_name,
            "referee_count": referee_count,
            "total_arrangements": total_arrangements,
            "checked_in": checked_in,
            "attendance_rate": round(checked_in / total_arrangements * 100, 2) if total_arrangements > 0 else 0,
        }


class RefereeArrangementService:
    """执裁安排服务类"""
    
    @staticmethod
    def get_today_arrangements():
        """获取今日所有执裁安排"""
        today = timezone.now().date()
        return RefereeArrangement.objects.filter(
            arrange_date__date=today
        ).order_by("arrange_date")
    
    @staticmethod
    def get_upcoming_arrangements(days=7):
        """获取未来N天的执裁安排"""
        start = timezone.now()
        end = start + timedelta(days=days)
        return RefereeArrangement.objects.filter(
            arrange_date__gte=start,
            arrange_date__lte=end
        ).order_by("arrange_date")
    
    @staticmethod
    def batch_check_in(arrangement_ids):
        """批量签到"""
        arrangements = RefereeArrangement.objects.filter(id__in=arrangement_ids)
        updated = arrangements.update(
            check_in_status="已签到",
            update_time=timezone.now()
        )
        return updated
    
    @staticmethod
    def get_arrangement_statistics():
        """获取执裁安排统计"""
        total = RefereeArrangement.objects.count()
        by_status = RefereeArrangement.objects.values('check_in_status').annotate(
            count=Count('id')
        )
        
        today = RefereeArrangement.objects.filter(
            arrange_date__date=timezone.now().date()
        ).count()
        
        upcoming = RefereeArrangement.objects.filter(
            arrange_date__gte=timezone.now()
        ).count()
        
        return {
            "total": total,
            "by_status": list(by_status),
            "today": today,
            "upcoming": upcoming,
        }
    
    @staticmethod
    def check_conflicts(referee_id, arrange_date, exclude_arrangement_id=None):
        """检查执裁安排时间冲突"""
        query = Q(
            referee_id=referee_id,
            arrange_date=arrange_date
        )
        
        if exclude_arrangement_id:
            query &= ~Q(id=exclude_arrangement_id)
        
        conflicts = RefereeArrangement.objects.filter(query)
        return conflicts.exists(), conflicts

