from rest_framework import serializers

from .models import MedalHonor, Result


class ResultSerializer(serializers.ModelSerializer):
    athlete_name = serializers.SerializerMethodField()
    athlete_id = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()
    event_id = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Result
        fields = "__all__"
    
    def get_athlete_name(self, obj):
        try:
            if obj.apply and hasattr(obj.apply, 'athlete') and obj.apply.athlete:
                return obj.apply.athlete.name
        except Exception:
            pass
        return None
    
    def get_athlete_id(self, obj):
        try:
            if obj.apply and hasattr(obj.apply, 'athlete') and obj.apply.athlete:
                return obj.apply.athlete.id
        except Exception:
            pass
        return None
    
    def get_event_name(self, obj):
        try:
            if obj.apply and hasattr(obj.apply, 'event') and obj.apply.event:
                return obj.apply.event.event_name
        except Exception:
            pass
        return None
    
    def get_event_id(self, obj):
        try:
            if obj.apply and hasattr(obj.apply, 'event') and obj.apply.event:
                return obj.apply.event.id
        except Exception:
            pass
        return None
    
    def get_team_name(self, obj):
        try:
            if obj.apply and hasattr(obj.apply, 'athlete') and obj.apply.athlete:
                if hasattr(obj.apply.athlete, 'team') and obj.apply.athlete.team:
                    return obj.apply.athlete.team.team_name
        except Exception:
            pass
        return None


class MedalHonorSerializer(serializers.ModelSerializer):
    athlete_name = serializers.SerializerMethodField()
    team_name = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()
    
    class Meta:
        model = MedalHonor
        fields = "__all__"
    
    def get_athlete_name(self, obj):
        try:
            if obj.athlete:
                return obj.athlete.name
        except Exception:
            pass
        return None
    
    def get_team_name(self, obj):
        try:
            if obj.team:
                return obj.team.team_name
        except Exception:
            pass
        return None
    
    def get_event_name(self, obj):
        try:
            if obj.result and hasattr(obj.result, 'apply') and obj.result.apply:
                if hasattr(obj.result.apply, 'event') and obj.result.apply.event:
                    return obj.result.apply.event.event_name
        except Exception:
            pass
        return None

