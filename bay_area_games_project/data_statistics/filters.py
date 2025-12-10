import django_filters

from .models import DataReport


class DataReportFilter(django_filters.FilterSet):
    class Meta:
        model = DataReport
        fields = ["stat_dimension", "report_type", "export_status"]

