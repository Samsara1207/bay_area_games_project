"""
成绩管理业务逻辑服务
"""
import re
from decimal import Decimal
from typing import List, Optional

from django.db import transaction
from django.db.models import Q

from .models import MedalHonor, Result


class ResultService:
    """成绩管理服务"""

    @staticmethod
    def calculate_ranking(event_id: int, round_type: Optional[str] = None) -> None:
        """
        自动计算排名
        根据成绩值自动排序并更新排名字段
        """
        from event_management.models import Event

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return

        # 获取该项目的所有成绩
        results = Result.objects.filter(apply__event_id=event_id)
        if round_type:
            results = results.filter(round=round_type)

        if not results.exists():
            return

        # 根据项目类型判断排序方式
        # 时间类项目（越小越好）：短跑、游泳等
        # 距离类项目（越大越好）：跳远、跳高等
        # 分数类项目（越大越好）：球类、体操等

        event_type = event.event_type.lower()
        is_time_based = any(keyword in event_type for keyword in ["短跑", "长跑", "游泳", "竞走", "时间"])

        # 解析成绩值并排序
        result_list = []
        for result in results:
            try:
                # 尝试解析成绩值
                value = ResultService._parse_result_value(result.result_value, is_time_based)
                result_list.append((result, value))
            except (ValueError, AttributeError):
                # 如果无法解析，使用原始值
                result_list.append((result, float("inf") if is_time_based else float("-inf")))

        # 排序：时间类越小越好，其他越大越好
        result_list.sort(key=lambda x: x[1], reverse=not is_time_based)

        # 更新排名
        with transaction.atomic():
            for rank, (result, _) in enumerate(result_list, start=1):
                result.ranking = rank
                result.save(update_fields=["ranking"])

    @staticmethod
    def _parse_result_value(result_value: str, is_time_based: bool) -> float:
        """解析成绩值"""
        if not result_value:
            return float("inf") if is_time_based else float("-inf")

        # 时间格式：如 "10.5秒"、"1分50秒"、"1:50.5"
        if is_time_based:
            # 秒数格式
            if "秒" in result_value:
                seconds = re.findall(r"(\d+\.?\d*)", result_value)
                if seconds:
                    return float(seconds[0])
            # 分:秒格式
            elif ":" in result_value:
                parts = result_value.split(":")
                if len(parts) == 2:
                    return float(parts[0]) * 60 + float(parts[1])
            # 纯数字（假设是秒）
            else:
                try:
                    return float(result_value)
                except ValueError:
                    pass

        # 距离/分数格式：如 "5.5米"、"90分"
        else:
            numbers = re.findall(r"(\d+\.?\d*)", result_value)
            if numbers:
                return float(numbers[0])

        return float("inf") if is_time_based else float("-inf")

    @staticmethod
    def check_record(result_id: int) -> bool:
        """
        检查是否破纪录
        这里简化处理，实际应该查询历史纪录数据库
        """
        try:
            result = Result.objects.get(pk=result_id)
        except Result.DoesNotExist:
            return False

        # 简化逻辑：如果成绩值包含特定标记或排名第一且成绩突出，标记为破纪录
        # 实际应该查询历史最佳成绩数据库
        if result.ranking == 1 and result.result_value:
            # 这里可以添加更复杂的判断逻辑
            result.is_record = "是"
            result.save(update_fields=["is_record"])
            return True

        return False

    @staticmethod
    def auto_award_medals(event_id: int) -> None:
        """
        自动颁发奖牌
        根据排名自动创建奖牌记录
        """
        from event_management.models import Event

        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return

        # 获取决赛成绩的前三名
        results = Result.objects.filter(
            apply__event_id=event_id, round="决赛", ranking__lte=3, ranking__isnull=False
        ).order_by("ranking")

        medal_types = {1: "金牌", 2: "银牌", 3: "铜牌"}

        with transaction.atomic():
            for result in results:
                # 检查是否已有奖牌记录
                if not MedalHonor.objects.filter(result=result).exists():
                    athlete = result.apply.athlete
                    team = athlete.team

                    MedalHonor.objects.create(
                        medal_type=medal_types.get(result.ranking, "铜牌"),
                        athlete=athlete,
                        team=team,
                        result=result,
                        public_status="已公示",
                    )


class QualificationService:
    """资格审核服务"""

    @staticmethod
    def auto_qualify_athlete(athlete_id: int) -> bool:
        """
        自动审核运动员资格
        检查必要信息是否完整
        """
        from basic_info.models import Athlete

        try:
            athlete = Athlete.objects.get(pk=athlete_id)
        except Athlete.DoesNotExist:
            return False

        # 检查必要信息
        required_fields = [
            athlete.name,
            athlete.id_card,
            athlete.health_status,
            athlete.doping_test,
        ]

        if all(required_fields) and athlete.doping_test == "合格":
            athlete.qualification_status = "已审核"
            athlete.save(update_fields=["qualification_status"])
            return True

        return False

    @staticmethod
    def reject_athlete(athlete_id: int, reason: str = "") -> bool:
        """驳回运动员资格"""
        from basic_info.models import Athlete

        try:
            athlete = Athlete.objects.get(pk=athlete_id)
            athlete.qualification_status = "驳回"
            athlete.save(update_fields=["qualification_status"])
            return True
        except Athlete.DoesNotExist:
            return False

