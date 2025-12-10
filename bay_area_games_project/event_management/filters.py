import django_filters

from .models import AthleteEvent, Event, Group, Venue


class VenueFilter(django_filters.FilterSet):
    class Meta:
        model = Venue
        fields = ["venue_name", "facility_status"]


class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = ["event_type", "gender_limit", "venue", "bay_feature"]


class GroupFilter(django_filters.FilterSet):
    class Meta:
        model = Group
        fields = ["event", "disability_integration"]


class AthleteEventFilter(django_filters.FilterSet):
    class Meta:
        model = AthleteEvent
        fields = ["athlete", "event", "group", "apply_status"]

