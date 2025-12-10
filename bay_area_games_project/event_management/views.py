from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import AthleteEventFilter, EventFilter, GroupFilter, VenueFilter
from .models import AthleteEvent, Event, Group, Venue
from .serializers import AthleteEventSerializer, EventSerializer, GroupSerializer, VenueSerializer


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all().order_by("-create_time")
    serializer_class = VenueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VenueFilter
    search_fields = ["venue_name", "address", "manager_name"]
    ordering_fields = ["create_time", "update_time"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("-create_time")
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ["event_name", "event_type"]
    ordering_fields = ["event_time", "create_time"]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("-create_time")
    serializer_class = GroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = GroupFilter
    search_fields = ["group_name"]
    ordering_fields = ["create_time", "update_time"]


class AthleteEventViewSet(viewsets.ModelViewSet):
    queryset = AthleteEvent.objects.all().order_by("-create_time")
    serializer_class = AthleteEventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = AthleteEventFilter
    search_fields = ["athlete__name", "event__event_name"]
    ordering_fields = ["apply_time", "create_time"]
