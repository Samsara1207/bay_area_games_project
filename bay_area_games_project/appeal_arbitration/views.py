from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import AppealArbitrationFilter, AppealFilter, ArbitrationCommitteeFilter
from .models import Appeal, AppealArbitration, ArbitrationCommittee
from .serializers import AppealArbitrationSerializer, AppealSerializer, ArbitrationCommitteeSerializer


class AppealViewSet(viewsets.ModelViewSet):
    queryset = Appeal.objects.all().order_by("-submit_time")
    serializer_class = AppealSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AppealFilter
    search_fields = ["appeal_content", "status"]
    ordering_fields = ["submit_time", "create_time"]


class ArbitrationCommitteeViewSet(viewsets.ModelViewSet):
    queryset = ArbitrationCommittee.objects.all().order_by("-create_time")
    serializer_class = ArbitrationCommitteeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ArbitrationCommitteeFilter
    search_fields = ["committee_name"]
    ordering_fields = ["create_time", "update_time"]


class AppealArbitrationViewSet(viewsets.ModelViewSet):
    queryset = AppealArbitration.objects.all().order_by("-arbitration_time", "-create_time")
    serializer_class = AppealArbitrationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AppealArbitrationFilter
    search_fields = ["arbitration_result", "arbitration_basis"]
    ordering_fields = ["arbitration_time", "create_time"]
