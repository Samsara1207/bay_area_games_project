from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import DataReportFilter
from .models import DataReport
from .serializers import DataReportSerializer
from .services import StatisticsService


class DataReportViewSet(viewsets.ModelViewSet):
    queryset = DataReport.objects.all().order_by("-generate_time")
    serializer_class = DataReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DataReportFilter
    search_fields = ["stat_dimension", "stat_indicator"]
    ordering_fields = ["generate_time", "create_time"]

    @action(detail=False, methods=["post"])
    def generate_city_report(self, request):
        """生成城市统计报表"""
        report = StatisticsService.generate_city_report()
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def generate_event_report(self, request):
        """生成项目统计报表"""
        report = StatisticsService.generate_event_report()
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def generate_team_report(self, request):
        """生成代表队统计报表"""
        report = StatisticsService.generate_team_report()
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["get"])
    def daily_summary(self, request):
        """获取每日汇总数据"""
        summary = StatisticsService.generate_daily_summary()
        return Response(summary)
