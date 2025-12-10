from rest_framework import serializers

from .models import AthleteEvent, Event, Group, Venue


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class AthleteEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AthleteEvent
        fields = "__all__"

