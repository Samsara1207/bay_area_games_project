from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import AudienceTicketFilter, SponsorFilter, SponsorRightsFilter
from .models import AudienceTicket, Sponsor, SponsorRights
from .serializers import AudienceTicketSerializer, SponsorRightsSerializer, SponsorSerializer


class SponsorViewSet(viewsets.ModelViewSet):
    """赞助商管理视图集"""
    queryset = Sponsor.objects.all().order_by("-create_time")
    serializer_class = SponsorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SponsorFilter
    search_fields = ["sponsor_name", "bay_register_address", "contact_name"]
    ordering_fields = ["create_time", "update_time"]
    
    @action(detail=True, methods=["get"])
    def rights(self, request, pk=None):
        """获取赞助商的所有权益"""
        sponsor = self.get_object()
        rights = sponsor.rights.all().order_by("-create_time")
        serializer = SponsorRightsSerializer(rights, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """获取赞助商统计信息"""
        from django.db.models import Count, Sum
        stats = Sponsor.objects.aggregate(
            total=Count('id'),
            by_type=Count('id', distinct=True)
        )
        
        by_type = Sponsor.objects.values('sponsor_type').annotate(
            count=Count('id')
        )
        
        return Response({
            "total": stats['total'],
            "by_type": list(by_type),
        })


class SponsorRightsViewSet(viewsets.ModelViewSet):
    """赞助商权益管理视图集"""
    queryset = SponsorRights.objects.all().order_by("-create_time")
    serializer_class = SponsorRightsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = SponsorRightsFilter
    search_fields = ["rights_type", "bay_media_channel"]
    ordering_fields = ["exposure_count", "create_time"]
    
    @action(detail=True, methods=["post"])
    def update_exposure(self, request, pk=None):
        """更新曝光次数"""
        rights = self.get_object()
        increment = request.data.get("increment", 1)
        rights.exposure_count += increment
        rights.save(update_fields=["exposure_count", "update_time"])
        serializer = self.get_serializer(rights)
        return Response(serializer.data)
    
    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        """更新执行状态"""
        rights = self.get_object()
        new_status = request.data.get("rights_status")
        if new_status not in ["已执行", "未执行", "部分执行"]:
            return Response(
                {"error": "无效的状态值"},
                status=status.HTTP_400_BAD_REQUEST
            )
        rights.rights_status = new_status
        rights.save(update_fields=["rights_status", "update_time"])
        serializer = self.get_serializer(rights)
        return Response(serializer.data)


class AudienceTicketViewSet(viewsets.ModelViewSet):
    """观众票务管理视图集"""
    queryset = AudienceTicket.objects.all().order_by("-create_time")
    serializer_class = AudienceTicketSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AudienceTicketFilter
    search_fields = ["audience_name", "audience_id_card", "seat_no", "entry_verification_code"]
    ordering_fields = ["ticket_price", "entry_time", "create_time"]
    
    @action(detail=True, methods=["post"])
    def refund(self, request, pk=None):
        """退票"""
        ticket = self.get_object()
        if ticket.refund_status == "已退票":
            return Response(
                {"message": "该票已经退过了"},
                status=status.HTTP_200_OK
            )
        ticket.refund_status = "已退票"
        ticket.save(update_fields=["refund_status", "update_time"])
        serializer = self.get_serializer(ticket)
        return Response({
            "message": "退票成功",
            "data": serializer.data
        })
    
    @action(detail=True, methods=["post"])
    def confirm_notice(self, request, pk=None):
        """确认观赛须知"""
        ticket = self.get_object()
        ticket.notice_confirm_status = "已确认"
        ticket.save(update_fields=["notice_confirm_status", "update_time"])
        serializer = self.get_serializer(ticket)
        return Response({
            "message": "确认成功",
            "data": serializer.data
        })
    
    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """获取票务统计信息"""
        from django.db.models import Count, Sum
        from django.db.models import Q
        
        total = AudienceTicket.objects.count()
        sold = AudienceTicket.objects.filter(refund_status="未退票").count()
        refunded = AudienceTicket.objects.filter(refund_status="已退票").count()
        
        total_revenue = AudienceTicket.objects.filter(
            refund_status="未退票"
        ).aggregate(total=Sum('ticket_price'))['total'] or 0
        
        by_channel = AudienceTicket.objects.values('purchase_channel').annotate(
            count=Count('id')
        )
        
        return Response({
            "total": total,
            "sold": sold,
            "refunded": refunded,
            "total_revenue": float(total_revenue),
            "by_channel": list(by_channel),
        })
