from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .filters import AthleteFilter, TeamFilter
from .models import Athlete, Team
from .serializers import AthleteSerializer, TeamSerializer
from result_management.services import QualificationService


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by("-create_time")
    serializer_class = TeamSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TeamFilter
    search_fields = ["team_name", "leader_name", "region"]
    ordering_fields = ["create_time", "update_time"]
    
    def destroy(self, request, *args, **kwargs):
        """
        重写删除方法，确保级联删除所有相关数据
        删除顺序：MedalHonor -> Result -> AthleteEvent -> Athlete -> Team
        """
        instance = self.get_object()
        
        # 获取所有关联的运动员
        athletes = instance.athletes.all()
        athlete_ids = list(athletes.values_list('id', flat=True))
        
        # 使用事务确保数据一致性
        with transaction.atomic():
            # 1. 删除奖牌记录（通过 Result -> AthleteEvent -> Athlete 关联）
            from event_management.models import AthleteEvent
            from result_management.models import Result, MedalHonor
            
            if athlete_ids:
                # 获取所有相关的报名记录
                athlete_events = AthleteEvent.objects.filter(athlete_id__in=athlete_ids)
                apply_ids = list(athlete_events.values_list('id', flat=True))
                
                if apply_ids:
                    # 获取所有相关的成绩记录
                    results = Result.objects.filter(apply_id__in=apply_ids)
                    result_ids = list(results.values_list('id', flat=True))
                    
                    if result_ids:
                        # 删除奖牌记录
                        MedalHonor.objects.filter(result_id__in=result_ids).delete()
                        # 删除成绩记录
                        results.delete()
                    
                    # 删除报名记录
                    athlete_events.delete()
                
                # 2. 删除申诉记录（如果有）
                from appeal_arbitration.models import Appeal
                Appeal.objects.filter(athlete_id__in=athlete_ids).delete()
                
                # 3. 删除运动员记录（这会触发其他 CASCADE 删除）
                athletes.delete()
            
            # 4. 最后删除代表队
            instance.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class AthleteViewSet(viewsets.ModelViewSet):
    queryset = Athlete.objects.all().order_by("-create_time")
    serializer_class = AthleteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AthleteFilter
    search_fields = ["name", "id_card", "competition_id"]
    ordering_fields = ["create_time", "update_time"]

    @action(detail=True, methods=["post"])
    def auto_qualify(self, request, pk=None):
        """自动审核运动员资格"""
        success = QualificationService.auto_qualify_athlete(pk)
        if success:
            return Response({"message": "资格审核通过"})
        return Response({"error": "资格审核失败，请检查必要信息"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """驳回运动员资格"""
        reason = request.data.get("reason", "")
        success = QualificationService.reject_athlete(pk, reason)
        if success:
            return Response({"message": "资格已驳回"})
        return Response({"error": "操作失败"}, status=status.HTTP_400_BAD_REQUEST)
