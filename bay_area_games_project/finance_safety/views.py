from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import EpidemicSafetyFilter, FinanceFilter
from .models import EpidemicSafety, Finance
from .serializers import EpidemicSafetySerializer, FinanceSerializer


class FinanceViewSet(viewsets.ModelViewSet):
    queryset = Finance.objects.all().order_by("-create_time")
    serializer_class = FinanceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = FinanceFilter
    search_fields = ["related_no", "payer_payee"]
    ordering_fields = ["amount", "create_time"]


class EpidemicSafetyViewSet(viewsets.ModelViewSet):
    queryset = EpidemicSafety.objects.all().order_by("-create_time")
    serializer_class = EpidemicSafetySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EpidemicSafetyFilter
    search_fields = ["person_type"]
    ordering_fields = ["create_time", "temperature"]
