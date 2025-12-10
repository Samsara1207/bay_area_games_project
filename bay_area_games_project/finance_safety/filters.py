import django_filters

from .models import EpidemicSafety, Finance


class FinanceFilter(django_filters.FilterSet):
    class Meta:
        model = Finance
        fields = ["finance_type", "settle_status"]


class EpidemicSafetyFilter(django_filters.FilterSet):
    class Meta:
        model = EpidemicSafety
        fields = ["person_type", "safety_training_status"]

