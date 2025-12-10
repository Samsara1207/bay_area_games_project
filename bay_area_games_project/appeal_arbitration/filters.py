import django_filters

from .models import Appeal, AppealArbitration, ArbitrationCommittee


class AppealFilter(django_filters.FilterSet):
    class Meta:
        model = Appeal
        fields = ["athlete", "event", "status"]


class ArbitrationCommitteeFilter(django_filters.FilterSet):
    class Meta:
        model = ArbitrationCommittee
        fields = ["committee_name"]


class AppealArbitrationFilter(django_filters.FilterSet):
    class Meta:
        model = AppealArbitration
        fields = ["appeal", "committee"]

