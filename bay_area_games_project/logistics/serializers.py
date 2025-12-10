from rest_framework import serializers

from .models import LogisticsDetail, Supplier, Volunteer


class SupplierSerializer(serializers.ModelSerializer):
    """供应商序列化器"""
    logistics_count = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    avg_satisfaction = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = "__all__"
    
    def get_logistics_count(self, obj):
        """获取后勤保障记录数量"""
        return obj.logistics.count()
    
    def get_total_cost(self, obj):
        """获取总费用"""
        from django.db.models import Sum
        total = obj.logistics.aggregate(total=Sum('cost_amount'))['total']
        return float(total) if total else 0
    
    def get_avg_satisfaction(self, obj):
        """获取平均满意度"""
        from django.db.models import Avg
        avg = obj.logistics.exclude(satisfaction_score__isnull=True).aggregate(
            avg=Avg('satisfaction_score')
        )['avg']
        return round(float(avg), 1) if avg else None


class LogisticsDetailSerializer(serializers.ModelSerializer):
    """后勤保障明细序列化器"""
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    supplier_id = serializers.IntegerField(source='supplier.id', read_only=True)
    service_object_name = serializers.SerializerMethodField()
    
    class Meta:
        model = LogisticsDetail
        fields = "__all__"
    
    def get_service_object_name(self, obj):
        """获取服务对象名称"""
        if obj.service_object_type == "运动员":
            from basic_info.models import Athlete
            try:
                athlete = Athlete.objects.get(id=obj.service_object_id)
                return athlete.name
            except Athlete.DoesNotExist:
                return f"运动员#{obj.service_object_id}"
        elif obj.service_object_type == "裁判":
            from referee_management.models import Referee
            try:
                referee = Referee.objects.get(id=obj.service_object_id)
                return referee.name
            except Referee.DoesNotExist:
                return f"裁判#{obj.service_object_id}"
        elif obj.service_object_type == "工作人员":
            return f"工作人员#{obj.service_object_id}"
        return f"{obj.service_object_type}#{obj.service_object_id}"


class VolunteerSerializer(serializers.ModelSerializer):
    """志愿者序列化器"""
    
    class Meta:
        model = Volunteer
        fields = "__all__"

