from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Avg

from .filters import LogisticsDetailFilter, SupplierFilter, VolunteerFilter
from .models import LogisticsDetail, Supplier, Volunteer
from .serializers import LogisticsDetailSerializer, SupplierSerializer, VolunteerSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    """供应商管理视图集"""
    queryset = Supplier.objects.all().order_by("-create_time")
    serializer_class = SupplierSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SupplierFilter
    search_fields = ["supplier_name", "service_type", "contact_name"]
    ordering_fields = ["create_time", "update_time", "performance_score"]
    
    @action(detail=True, methods=["get"])
    def logistics(self, request, pk=None):
        """获取供应商的所有后勤保障记录"""
        supplier = self.get_object()
        logistics = supplier.logistics.all().order_by("-create_time")
        serializer = LogisticsDetailSerializer(logistics, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """获取供应商统计信息"""
        total = Supplier.objects.count()
        by_type = Supplier.objects.values('service_type').annotate(
            count=Count('id')
        )
        
        return Response({
            "total": total,
            "by_type": list(by_type),
        })


class LogisticsDetailViewSet(viewsets.ModelViewSet):
    """后勤保障明细管理视图集"""
    queryset = LogisticsDetail.objects.all().order_by("-create_time")
    serializer_class = LogisticsDetailSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = LogisticsDetailFilter
    search_fields = ["service_no", "staff_name"]
    ordering_fields = ["service_time", "create_time", "cost_amount"]
    
    @action(detail=True, methods=["post"])
    def update_satisfaction(self, request, pk=None):
        """更新满意度评分"""
        logistics = self.get_object()
        score = request.data.get("satisfaction_score")
        
        if score is None:
            return Response(
                {"error": "缺少满意度评分"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            score = int(score)
            if score < 1 or score > 5:
                return Response(
                    {"error": "满意度评分应在1-5之间"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "无效的评分值"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logistics.satisfaction_score = score
        logistics.save(update_fields=["satisfaction_score", "update_time"])
        serializer = self.get_serializer(logistics)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """获取后勤保障统计信息"""
        total = LogisticsDetail.objects.count()
        by_type = LogisticsDetail.objects.values('service_type').annotate(
            count=Count('id')
        )
        
        total_cost = LogisticsDetail.objects.aggregate(
            total=Sum('cost_amount')
        )['total'] or 0
        
        avg_satisfaction = LogisticsDetail.objects.exclude(
            satisfaction_score__isnull=True
        ).aggregate(
            avg=Avg('satisfaction_score')
        )['avg']
        
        return Response({
            "total": total,
            "by_type": list(by_type),
            "total_cost": float(total_cost),
            "avg_satisfaction": round(float(avg_satisfaction), 1) if avg_satisfaction else None,
        })


class VolunteerViewSet(viewsets.ModelViewSet):
    """志愿者管理视图集"""
    queryset = Volunteer.objects.all().order_by("-create_time")
    serializer_class = VolunteerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VolunteerFilter
    search_fields = ["name", "bay_school_company", "service_post", "phone"]
    ordering_fields = ["create_time", "working_hours"]
    
    @action(detail=True, methods=["post"])
    def complete_training(self, request, pk=None):
        """完成培训"""
        volunteer = self.get_object()
        volunteer.training_status = "已培训"
        volunteer.save(update_fields=["training_status", "update_time"])
        serializer = self.get_serializer(volunteer)
        return Response({
            "message": "培训状态已更新",
            "data": serializer.data
        })
    
    @action(detail=True, methods=["post"])
    def add_working_hours(self, request, pk=None):
        """增加服务工时"""
        volunteer = self.get_object()
        hours = request.data.get("hours", 0)
        
        try:
            hours = float(hours)
            if hours < 0:
                return Response(
                    {"error": "工时不能为负数"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "无效的工时值"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        volunteer.working_hours += hours
        volunteer.save(update_fields=["working_hours", "update_time"])
        serializer = self.get_serializer(volunteer)
        return Response({
            "message": "工时已更新",
            "data": serializer.data
        })
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """获取志愿者统计信息"""
        total = Volunteer.objects.count()
        trained = Volunteer.objects.filter(training_status="已培训").count()
        
        total_hours = Volunteer.objects.aggregate(
            total=Sum('working_hours')
        )['total'] or 0
        
        by_post = Volunteer.objects.values('service_post').annotate(
            count=Count('id')
        )
        
        return Response({
            "total": total,
            "trained": trained,
            "untrained": total - trained,
            "total_hours": float(total_hours),
            "by_post": list(by_post),
        })
