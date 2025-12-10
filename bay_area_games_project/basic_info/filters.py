import django_filters

from .models import Athlete, Team


class TeamFilter(django_filters.FilterSet):
    class Meta:
        model = Team
        fields = ["region", "city_code", "team_name"]


class AthleteFilter(django_filters.FilterSet):
    class Meta:
        model = Athlete
        fields = ["team", "bay_area_hukou", "qualification_status", "gender"]

