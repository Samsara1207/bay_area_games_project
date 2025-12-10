import django_filters

from .models import EventOperation, Schedule


class ScheduleFilter(django_filters.FilterSet):
    class Meta:
        model = Schedule
        fields = ["event", "venue", "schedule_date", "status"]


class EventOperationFilter(django_filters.FilterSet):
    class Meta:
        model = EventOperation
        fields = ["event", "operation_link", "status", "bay_approval_status"]

