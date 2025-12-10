from rest_framework import serializers

from .models import EventOperation, Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class EventOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventOperation
        fields = "__all__"

