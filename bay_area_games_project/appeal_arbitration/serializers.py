from rest_framework import serializers

from .models import Appeal, AppealArbitration, ArbitrationCommittee


class AppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeal
        fields = "__all__"


class ArbitrationCommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArbitrationCommittee
        fields = "__all__"


class AppealArbitrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppealArbitration
        fields = "__all__"

