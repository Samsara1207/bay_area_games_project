import django_filters
from django.db import models

from .models import LogisticsDetail, Supplier, Volunteer


class SupplierFilter(django_filters.FilterSet):
    """供应商过滤器"""
    service_type = django_filters.CharFilter(field_name="service_type", lookup_expr="exact")
    supplier_name__icontains = django_filters.CharFilter(field_name="supplier_name", lookup_expr="icontains")
    performance_score__gte = django_filters.NumberFilter(field_name="performance_score", lookup_expr="gte")
    
    class Meta:
        model = Supplier
        fields = ["service_type", "supplier_name"]


class LogisticsDetailFilter(django_filters.FilterSet):
    """后勤保障明细过滤器"""
    service_type = django_filters.CharFilter(field_name="service_type", lookup_expr="exact")
    service_object_type = django_filters.CharFilter(field_name="service_object_type", lookup_expr="exact")
    supplier = django_filters.NumberFilter(field_name="supplier", lookup_expr="exact")
    service_time__gte = django_filters.DateTimeFilter(field_name="service_time", lookup_expr="gte")
    service_time__lte = django_filters.DateTimeFilter(field_name="service_time", lookup_expr="lte")
    cost_amount__gte = django_filters.NumberFilter(field_name="cost_amount", lookup_expr="gte")
    cost_amount__lte = django_filters.NumberFilter(field_name="cost_amount", lookup_expr="lte")
    
    class Meta:
        model = LogisticsDetail
        fields = ["service_type", "service_object_type", "supplier", "service_time", "cost_amount"]


class VolunteerFilter(django_filters.FilterSet):
    """志愿者过滤器"""
    service_post = django_filters.CharFilter(field_name="service_post", lookup_expr="exact")
    training_status = django_filters.CharFilter(field_name="training_status", lookup_expr="exact")
    gender = django_filters.CharFilter(field_name="gender", lookup_expr="exact")
    bay_school_company__icontains = django_filters.CharFilter(field_name="bay_school_company", lookup_expr="icontains")
    
    class Meta:
        model = Volunteer
        fields = ["service_post", "training_status", "gender", "bay_school_company"]

