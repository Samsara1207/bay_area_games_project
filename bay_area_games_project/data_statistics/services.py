"""
数据统计服务
"""
import json
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List

from django.db.models import Count, Q, Sum
from django.utils import timezone

from .models import DataReport


class StatisticsService:
    """数据统计服务"""

    @staticmethod
    def generate_city_report() -> DataReport:
        """生成大湾区城市统计报表"""
        from basic_info.models import Team
        from result_management.models import MedalHonor

        # 统计各城市参赛人数和奖牌数
        city_stats = {}
        teams = Team.objects.all()

        for team in teams:
            city = team.region
            if city not in city_stats:
                city_stats[city] = {"参赛人数": 0, "金牌数": 0, "银牌数": 0, "铜牌数": 0, "总奖牌数": 0}

            # 统计参赛人数
            athlete_count = team.athletes.filter(qualification_status="已审核").count()
            city_stats[city]["参赛人数"] += athlete_count

            # 统计奖牌数
            medals = MedalHonor.objects.filter(team=team, public_status="已公示")
            city_stats[city]["金牌数"] += medals.filter(medal_type="金牌").count()
            city_stats[city]["银牌数"] += medals.filter(medal_type="银牌").count()
            city_stats[city]["铜牌数"] += medals.filter(medal_type="铜牌").count()
            city_stats[city]["总奖牌数"] += medals.count()

        stat_data = json.dumps(city_stats, ensure_ascii=False)

        return DataReport.objects.create(
            stat_dimension="大湾区城市",
            stat_indicator="参赛人数、奖牌数",
            report_type="总榜",
            stat_data=stat_data,
        )

    @staticmethod
    def generate_event_report() -> DataReport:
        """生成项目统计报表"""
        from event_management.models import Event
        from result_management.models import Result

        event_stats = {}
        events = Event.objects.all()

        for event in events:
            results = Result.objects.filter(apply__event=event)
            if results.exists():
                best_result = results.order_by("ranking").first()
                record_count = results.filter(is_record="是").count()

                event_stats[event.event_name] = {
                    "最好成绩": best_result.result_value if best_result else "暂无",
                    "破纪录数": record_count,
                    "参赛人数": results.count(),
                }

        stat_data = json.dumps(event_stats, ensure_ascii=False)

        return DataReport.objects.create(
            stat_dimension="项目",
            stat_indicator="成绩、破纪录数",
            report_type="周报",
            stat_data=stat_data,
        )

    @staticmethod
    def generate_team_report() -> DataReport:
        """生成代表队统计报表"""
        from basic_info.models import Team
        from result_management.models import MedalHonor, Result

        team_stats = {}
        teams = Team.objects.all()

        for team in teams:
            # 统计积分和获奖数
            medals = MedalHonor.objects.filter(team=team, public_status="已公示")
            results = Result.objects.filter(apply__athlete__team=team)

            total_score = sum(r.score_value or 0 for r in results)
            medal_count = medals.count()

            team_stats[team.team_name] = {"积分": total_score, "获奖数": medal_count}

        stat_data = json.dumps(team_stats, ensure_ascii=False)

        return DataReport.objects.create(
            stat_dimension="代表队",
            stat_indicator="积分、获奖数",
            report_type="日报",
            stat_data=stat_data,
        )

    @staticmethod
    def generate_daily_summary() -> Dict:
        """生成每日汇总数据"""
        from basic_info.models import Athlete, Team
        from event_management.models import Event
        from result_management.models import MedalHonor, Result

        today = timezone.now().date()

        summary = {
            "日期": today.strftime("%Y-%m-%d"),
            "代表队数": Team.objects.count(),
            "运动员总数": Athlete.objects.count(),
            "已审核运动员": Athlete.objects.filter(qualification_status="已审核").count(),
            "比赛项目数": Event.objects.count(),
            "已完成项目": Event.objects.filter(event_time__date__lte=today).count(),
            "总奖牌数": MedalHonor.objects.filter(public_status="已公示").count(),
            "破纪录数": Result.objects.filter(is_record="是").count(),
        }

        return summary

