from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RefereeArrangementFilter, RefereeFilter, RefereeGroupFilter
from .models import Referee, RefereeArrangement, RefereeGroup
from .serializers import RefereeArrangementSerializer, RefereeGroupSerializer, RefereeSerializer


class RefereeViewSet(viewsets.ModelViewSet):
    """裁判管理视图集"""
    queryset = Referee.objects.all().order_by("-create_time")
    serializer_class = RefereeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RefereeFilter
    search_fields = ["name", "charge_event", "multi_language", "phone"]
    ordering_fields = ["create_time", "update_time", "referee_level"]
    
    @action(detail=True, methods=["get"])
    def arrangements(self, request, pk=None):
        """获取裁判的所有执裁安排"""
        referee = self.get_object()
        arrangements = referee.arrangements.all().order_by("-arrange_date")
        serializer = RefereeArrangementSerializer(arrangements, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        """获取裁判的执裁历史"""
        referee = self.get_object()
        arrangements = referee.arrangements.filter(
            check_in_status="已签到"
        ).order_by("-arrange_date")
        
        history_data = []
        for arr in arrangements:
            history_data.append({
                "id": arr.id,
                "event_name": arr.event.event_name,
                "arrange_date": arr.arrange_date,
                "position": arr.position,
                "evaluation": arr.evaluation,
            })
        
        return Response({
            "referee_name": referee.name,
            "referee_level": referee.referee_level,
            "total_arrangements": arrangements.count(),
            "history": history_data,
        })
    
    @action(detail=False, methods=["get"])
    def by_level(self, request):
        """按等级统计裁判"""
        from django.db.models import Count
        stats = Referee.objects.values('referee_level').annotate(
            count=Count('id')
        ).order_by('referee_level')
        return Response(list(stats))
    
    @action(detail=False, methods=["get"])
    def bay_certified(self, request):
        """获取所有大湾区认证的裁判"""
        referees = Referee.objects.filter(bay_cert="有")
        serializer = self.get_serializer(referees, many=True)
        return Response(serializer.data)


class RefereeGroupViewSet(viewsets.ModelViewSet):
    """裁判组管理视图集"""
    queryset = RefereeGroup.objects.all().order_by("-create_time")
    serializer_class = RefereeGroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RefereeGroupFilter
    search_fields = ["group_name", "event__event_name"]
    ordering_fields = ["create_time", "update_time"]
    
    @action(detail=True, methods=["get"])
    def members(self, request, pk=None):
        """获取裁判组的所有成员"""
        group = self.get_object()
        # 获取所有不重复的裁判
        referee_ids = group.arrangements.values_list('referee', flat=True).distinct()
        referees = Referee.objects.filter(id__in=referee_ids)
        serializer = RefereeSerializer(referees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"])
    def arrangements(self, request, pk=None):
        """获取裁判组的所有执裁安排"""
        group = self.get_object()
        arrangements = group.arrangements.all().order_by("-arrange_date")
        serializer = RefereeArrangementSerializer(arrangements, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def add_referee(self, request, pk=None):
        """向裁判组添加裁判"""
        group = self.get_object()
        referee_id = request.data.get("referee_id")
        arrange_date = request.data.get("arrange_date")
        position = request.data.get("position", "")
        
        if not referee_id or not arrange_date:
            return Response(
                {"error": "缺少必要参数：referee_id 和 arrange_date"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            referee = Referee.objects.get(id=referee_id)
            arrangement = RefereeArrangement.objects.create(
                referee_group=group,
                referee=referee,
                event=group.event,
                arrange_date=arrange_date,
                position=position,
            )
            serializer = RefereeArrangementSerializer(arrangement)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Referee.DoesNotExist:
            return Response(
                {"error": "裁判不存在"},
                status=status.HTTP_404_NOT_FOUND
            )


class RefereeArrangementViewSet(viewsets.ModelViewSet):
    """执裁安排管理视图集"""
    queryset = RefereeArrangement.objects.all().order_by("-arrange_date")
    serializer_class = RefereeArrangementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = RefereeArrangementFilter
    search_fields = ["position", "referee__name", "event__event_name"]
    ordering_fields = ["arrange_date", "create_time"]
    
    @action(detail=True, methods=["post"])
    def check_in(self, request, pk=None):
        """裁判签到"""
        arrangement = self.get_object()
        if arrangement.check_in_status == "已签到":
            return Response(
                {"message": "已经签到过了", "status": "已签到"},
                status=status.HTTP_200_OK
            )
        
        arrangement.check_in_status = "已签到"
        arrangement.save(update_fields=["check_in_status", "update_time"])
        
        serializer = self.get_serializer(arrangement)
        return Response({
            "message": "签到成功",
            "data": serializer.data
        })
    
    @action(detail=True, methods=["post"])
    def evaluate(self, request, pk=None):
        """执裁评价"""
        arrangement = self.get_object()
        evaluation = request.data.get("evaluation", "")
        
        if not evaluation:
            return Response(
                {"error": "评价内容不能为空"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        arrangement.evaluation = evaluation
        arrangement.save(update_fields=["evaluation", "update_time"])
        
        serializer = self.get_serializer(arrangement)
        return Response({
            "message": "评价已保存",
            "data": serializer.data
        })
    
    @action(detail=False, methods=["get"])
    def today(self, request):
        """获取今日的执裁安排"""
        from django.utils import timezone
        today = timezone.now().date()
        arrangements = RefereeArrangement.objects.filter(
            arrange_date__date=today
        ).order_by("arrange_date")
        serializer = self.get_serializer(arrangements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        """获取即将进行的执裁安排"""
        from django.utils import timezone
        now = timezone.now()
        arrangements = RefereeArrangement.objects.filter(
            arrange_date__gte=now
        ).order_by("arrange_date")[:10]  # 最近10条
        serializer = self.get_serializer(arrangements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def by_status(self, request):
        """按签到状态统计"""
        from django.db.models import Count
        stats = RefereeArrangement.objects.values('check_in_status').annotate(
            count=Count('id')
        ).order_by('check_in_status')
        return Response(list(stats))
