from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import EventOperationFilter, ScheduleFilter
from .models import EventOperation, Schedule
from .serializers import EventOperationSerializer, ScheduleSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by("-schedule_date", "-time_slot")
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ScheduleFilter
    search_fields = ["time_slot"]
    ordering_fields = ["schedule_date", "time_slot", "create_time"]


class EventOperationViewSet(viewsets.ModelViewSet):
    queryset = EventOperation.objects.all().order_by("-create_time")
    serializer_class = EventOperationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventOperationFilter
    search_fields = ["operation_link", "status"]
    ordering_fields = ["start_time", "create_time"]
