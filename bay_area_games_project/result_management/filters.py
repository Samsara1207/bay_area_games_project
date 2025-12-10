import django_filters

from .models import MedalHonor, Result


class ResultFilter(django_filters.FilterSet):
    class Meta:
        model = Result
        fields = ["apply", "ranking", "is_record", "record_cert_status"]


class MedalHonorFilter(django_filters.FilterSet):
    class Meta:
        model = MedalHonor
        fields = ["medal_type", "athlete", "team", "result", "public_status"]

