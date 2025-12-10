import django_filters
from django.db import models

from .models import Referee, RefereeArrangement, RefereeGroup


class RefereeFilter(django_filters.FilterSet):
    """裁判过滤器"""
    referee_level = django_filters.CharFilter(field_name="referee_level", lookup_expr="exact")
    bay_cert = django_filters.CharFilter(field_name="bay_cert", lookup_expr="exact")
    gender = django_filters.CharFilter(field_name="gender", lookup_expr="exact")
    charge_event__icontains = django_filters.CharFilter(field_name="charge_event", lookup_expr="icontains")
    
    class Meta:
        model = Referee
        fields = ["referee_level", "bay_cert", "gender", "charge_event"]


class RefereeGroupFilter(django_filters.FilterSet):
    """裁判组过滤器"""
    event = django_filters.NumberFilter(field_name="event", lookup_expr="exact")
    event__event_name = django_filters.CharFilter(field_name="event__event_name", lookup_expr="icontains")
    leader_referee = django_filters.NumberFilter(field_name="leader_referee", lookup_expr="exact")
    leader_referee__name = django_filters.CharFilter(field_name="leader_referee__name", lookup_expr="icontains")
    
    class Meta:
        model = RefereeGroup
        fields = ["event", "leader_referee"]


class RefereeArrangementFilter(django_filters.FilterSet):
    """执裁安排过滤器"""
    referee_group = django_filters.NumberFilter(field_name="referee_group", lookup_expr="exact")
    referee = django_filters.NumberFilter(field_name="referee", lookup_expr="exact")
    referee__name = django_filters.CharFilter(field_name="referee__name", lookup_expr="icontains")
    event = django_filters.NumberFilter(field_name="event", lookup_expr="exact")
    event__event_name = django_filters.CharFilter(field_name="event__event_name", lookup_expr="icontains")
    check_in_status = django_filters.CharFilter(field_name="check_in_status", lookup_expr="exact")
    arrange_date__gte = django_filters.DateTimeFilter(field_name="arrange_date", lookup_expr="gte")
    arrange_date__lte = django_filters.DateTimeFilter(field_name="arrange_date", lookup_expr="lte")
    position__icontains = django_filters.CharFilter(field_name="position", lookup_expr="icontains")
    
    class Meta:
        model = RefereeArrangement
        fields = ["referee_group", "referee", "event", "check_in_status", "arrange_date", "position"]

