from rest_framework import serializers

from .models import EpidemicSafety, Finance


class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Finance
        fields = "__all__"


class EpidemicSafetySerializer(serializers.ModelSerializer):
    class Meta:
        model = EpidemicSafety
        fields = "__all__"

