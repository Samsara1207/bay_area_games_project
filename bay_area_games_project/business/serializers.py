from rest_framework import serializers

from .models import AudienceTicket, Sponsor, SponsorRights


class SponsorSerializer(serializers.ModelSerializer):
    """赞助商序列化器"""
    rights_count = serializers.SerializerMethodField()
    total_exposure = serializers.SerializerMethodField()
    
    class Meta:
        model = Sponsor
        fields = "__all__"
    
    def get_rights_count(self, obj):
        """获取权益数量"""
        return obj.rights.count()
    
    def get_total_exposure(self, obj):
        """获取总曝光次数"""
        return sum(right.exposure_count for right in obj.rights.all())


class SponsorRightsSerializer(serializers.ModelSerializer):
    """赞助商权益序列化器"""
    sponsor_name = serializers.CharField(source='sponsor.sponsor_name', read_only=True)
    sponsor_id = serializers.IntegerField(source='sponsor.id', read_only=True)
    event_name = serializers.CharField(source='event.event_name', read_only=True)
    event_id = serializers.IntegerField(source='event.id', read_only=True)
    finance_id = serializers.IntegerField(source='finance.id', read_only=True)
    
    class Meta:
        model = SponsorRights
        fields = "__all__"


class AudienceTicketSerializer(serializers.ModelSerializer):
    """观众票务序列化器"""
    event_name = serializers.CharField(source='event.event_name', read_only=True)
    event_id = serializers.IntegerField(source='event.id', read_only=True)
    event_time = serializers.DateTimeField(source='event.event_time', read_only=True)
    
    class Meta:
        model = AudienceTicket
        fields = "__all__"

