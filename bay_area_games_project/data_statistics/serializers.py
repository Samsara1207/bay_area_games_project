from rest_framework import serializers

from .models import DataReport


class DataReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataReport
        fields = "__all__"

