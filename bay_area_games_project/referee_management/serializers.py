from rest_framework import serializers

from .models import Referee, RefereeArrangement, RefereeGroup


class RefereeSerializer(serializers.ModelSerializer):
    """裁判序列化器"""
    arrangements_count = serializers.SerializerMethodField()
    lead_groups_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Referee
        fields = "__all__"
    
    def get_arrangements_count(self, obj):
        """获取执裁安排数量"""
        return obj.arrangements.count()
    
    def get_lead_groups_count(self, obj):
        """获取担任组长的裁判组数量"""
        return obj.lead_groups.count()


class RefereeGroupSerializer(serializers.ModelSerializer):
    """裁判组序列化器"""
    leader_referee_name = serializers.CharField(source='leader_referee.name', read_only=True)
    event_name = serializers.CharField(source='event.event_name', read_only=True)
    event_id = serializers.IntegerField(source='event.id', read_only=True)
    arrangements_count = serializers.SerializerMethodField()
    referees_count = serializers.SerializerMethodField()
    
    class Meta:
        model = RefereeGroup
        fields = "__all__"
    
    def get_arrangements_count(self, obj):
        """获取执裁安排数量"""
        return obj.arrangements.count()
    
    def get_referees_count(self, obj):
        """获取裁判组内裁判数量（去重）"""
        return obj.arrangements.values('referee').distinct().count()


class RefereeArrangementSerializer(serializers.ModelSerializer):
    """执裁安排序列化器"""
    referee_name = serializers.CharField(source='referee.name', read_only=True)
    referee_id = serializers.IntegerField(source='referee.id', read_only=True)
    referee_level = serializers.CharField(source='referee.referee_level', read_only=True)
    referee_phone = serializers.CharField(source='referee.phone', read_only=True)
    referee_group_name = serializers.CharField(source='referee_group.group_name', read_only=True)
    referee_group_id = serializers.IntegerField(source='referee_group.id', read_only=True)
    event_name = serializers.CharField(source='event.event_name', read_only=True)
    event_id = serializers.IntegerField(source='event.id', read_only=True)
    event_time = serializers.DateTimeField(source='event.event_time', read_only=True)
    
    class Meta:
        model = RefereeArrangement
        fields = "__all__"

