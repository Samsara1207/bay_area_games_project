from django.db import models


class Finance(models.Model):
    """财务结算"""

    FINANCE_TYPE = (("报名费", "报名费"), ("赞助费", "赞助费"), ("后勤费", "后勤费"), ("奖金", "奖金"), ("其他", "其他"))
    SETTLE_STATUS = (("已结算", "已结算"), ("未结算", "未结算"))

    finance_type = models.CharField(max_length=10, choices=FINANCE_TYPE, verbose_name="收支类型")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额")
    related_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="关联单号")
    payer_payee = models.CharField(max_length=100, null=True, blank=True, verbose_name="付款/收款方")
    settle_status = models.CharField(max_length=10, choices=SETTLE_STATUS, default="未结算", verbose_name="结算状态")
    bay_tax_record_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="税务备案号")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "财务结算"
        verbose_name_plural = "财务结算"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["finance_type"], name="idx_finance_type"),
            models.Index(fields=["related_no"], name="idx_finance_related"),
        ]

    def __str__(self) -> str:
        return f"{self.finance_type}-{self.amount}"


class EpidemicSafety(models.Model):
    """防疫安全"""

    PERSON_TYPE = (("运动员", "运动员"), ("观众", "观众"), ("工作人员", "工作人员"))
    TRAINING_STATUS = (("已培训", "已培训"), ("未培训", "未培训"))

    person_type = models.CharField(max_length=10, choices=PERSON_TYPE, verbose_name="人员类型")
    person_id = models.PositiveIntegerField(verbose_name="人员ID")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="体温")
    safety_training_status = models.CharField(
        max_length=10, choices=TRAINING_STATUS, default="未培训", verbose_name="安全培训状态"
    )
    emergency_record = models.TextField(null=True, blank=True, verbose_name="应急记录")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "防疫安全"
        verbose_name_plural = "防疫安全"
        ordering = ["-create_time"]
        indexes = [models.Index(fields=["person_type", "person_id"], name="idx_es_person")]

    def __str__(self) -> str:
        return f"{self.person_type}-{self.person_id}"
