from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import MedalHonorFilter, ResultFilter
from .models import MedalHonor, Result
from .serializers import MedalHonorSerializer, ResultSerializer
from .services import ResultService


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all().order_by("-create_time")
    serializer_class = ResultSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ResultFilter
    search_fields = ["result_value"]
    ordering_fields = ["ranking", "create_time"]

    def perform_create(self, serializer):
        """创建成绩后自动计算排名"""
        result = serializer.save()
        if result.apply and result.apply.event:
            ResultService.calculate_ranking(result.apply.event.id, result.round)
            # 检查是否破纪录
            ResultService.check_record(result.id)

    def perform_update(self, serializer):
        """更新成绩后重新计算排名"""
        result = serializer.save()
        if result.apply and result.apply.event:
            ResultService.calculate_ranking(result.apply.event.id, result.round)
            ResultService.check_record(result.id)

    @action(detail=False, methods=["post"])
    def calculate_ranking(self, request):
        """手动触发排名计算"""
        event_id = request.data.get("event_id")
        round_type = request.data.get("round_type")
        if event_id:
            ResultService.calculate_ranking(event_id, round_type)
            return Response({"message": "排名计算完成"})
        return Response({"error": "缺少event_id参数"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def auto_award_medals(self, request):
        """自动颁发奖牌"""
        event_id = request.data.get("event_id")
        if event_id:
            ResultService.auto_award_medals(event_id)
            return Response({"message": "奖牌颁发完成"})
        return Response({"error": "缺少event_id参数"}, status=status.HTTP_400_BAD_REQUEST)


class MedalHonorViewSet(viewsets.ModelViewSet):
    queryset = MedalHonor.objects.all().order_by("-create_time")
    serializer_class = MedalHonorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MedalHonorFilter
    search_fields = ["medal_type", "honor_cert_no", "award_guest"]
    ordering_fields = ["award_time", "create_time"]
