from django.db import models


class Supplier(models.Model):
    """供应商"""

    supplier_name = models.CharField(max_length=100, verbose_name="供应商名称")
    service_type = models.CharField(max_length=50, verbose_name="服务类型")
    bay_register_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="大湾区注册地址")
    qualification_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="资质证书地址")
    coop_period = models.CharField(max_length=50, null=True, blank=True, verbose_name="合作期限")
    contact_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="联系人")
    contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系电话")
    performance_score = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True, verbose_name="履约评分"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "供应商"
        verbose_name_plural = "供应商"
        ordering = ["-create_time"]
        indexes = [models.Index(fields=["service_type"], name="idx_supplier_service_type")]

    def __str__(self) -> str:
        return self.supplier_name


class LogisticsDetail(models.Model):
    """后勤保障明细"""

    SERVICE_TYPE = (("餐饮", "餐饮"), ("住宿", "住宿"), ("医疗", "医疗"), ("交通", "交通"), ("器材", "器材"))
    SERVICE_OBJECT_TYPE = (("运动员", "运动员"), ("裁判", "裁判"), ("工作人员", "工作人员"))

    service_type = models.CharField(max_length=10, choices=SERVICE_TYPE, verbose_name="保障类型")
    service_object_type = models.CharField(max_length=10, choices=SERVICE_OBJECT_TYPE, verbose_name="服务对象类型")
    service_object_id = models.PositiveIntegerField(verbose_name="服务对象ID")
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name="logistics", verbose_name="供应商"
    )
    service_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="服务单号")
    cost_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="费用金额")
    service_time = models.DateTimeField(null=True, blank=True, verbose_name="服务时间")
    staff_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="服务人员")
    satisfaction_score = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="满意度评分")
    exception_record = models.TextField(null=True, blank=True, verbose_name="异常记录")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "后勤保障明细"
        verbose_name_plural = "后勤保障明细"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["service_object_type", "service_object_id"], name="idx_logistics_object"),
            models.Index(fields=["supplier"], name="idx_logistics_supplier"),
        ]

    def __str__(self) -> str:
        return f"{self.service_type}-{self.service_no or ''}"


class Volunteer(models.Model):
    """志愿者"""

    GENDER = (("男", "男"), ("女", "女"), ("其他", "其他"))
    TRAINING_STATUS = (("已培训", "已培训"), ("未培训", "未培训"))

    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=2, choices=GENDER, verbose_name="性别")
    bay_school_company = models.CharField(max_length=100, null=True, blank=True, verbose_name="大湾区院校/单位")
    service_post = models.CharField(max_length=50, null=True, blank=True, verbose_name="服务岗位")
    service_time_slot = models.CharField(max_length=100, null=True, blank=True, verbose_name="服务时段")
    training_status = models.CharField(max_length=10, choices=TRAINING_STATUS, default="未培训", verbose_name="培训状态")
    working_hours = models.DecimalField(max_digits=4, decimal_places=1, default=0, verbose_name="服务工时")
    evaluation = models.CharField(max_length=255, null=True, blank=True, verbose_name="服务评价")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系电话")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "志愿者"
        verbose_name_plural = "志愿者"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["service_post"], name="idx_vol_service_post"),
            models.Index(fields=["training_status"], name="idx_vol_training"),
        ]

    def __str__(self) -> str:
        return self.name
