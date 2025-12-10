from django.db import models


class Appeal(models.Model):
    """申诉"""

    STATUS = (("待处理", "待处理"), ("已受理", "已受理"), ("已驳回", "已驳回"), ("已解决", "已解决"))

    athlete = models.ForeignKey(
        "basic_info.Athlete", on_delete=models.CASCADE, related_name="appeals", verbose_name="运动员"
    )
    event = models.ForeignKey(
        "event_management.Event", on_delete=models.CASCADE, related_name="appeals", verbose_name="项目"
    )
    appeal_content = models.TextField(verbose_name="申诉内容")
    submit_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")
    status = models.CharField(max_length=5, choices=STATUS, default="待处理", verbose_name="处理状态")
    result = models.TextField(null=True, blank=True, verbose_name="处理结果")
    handler_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="处理人编号")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "申诉"
        verbose_name_plural = "申诉"
        ordering = ["-submit_time"]
        indexes = [
            models.Index(fields=["athlete"], name="idx_appeal_athlete"),
            models.Index(fields=["event"], name="idx_appeal_event"),
            models.Index(fields=["status"], name="idx_appeal_status"),
        ]

    def __str__(self) -> str:
        return f"{self.athlete}-{self.event}-{self.status}"


class ArbitrationCommittee(models.Model):
    """仲裁委员会"""

    committee_name = models.CharField(max_length=100, verbose_name="委员会名称")
    member_ids = models.TextField(null=True, blank=True, verbose_name="成员ID列表")
    scope = models.CharField(max_length=255, null=True, blank=True, verbose_name="职责范围")
    contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系方式")
    arbitration_process_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="仲裁流程文档")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "仲裁委员会"
        verbose_name_plural = "仲裁委员会"
        ordering = ["-create_time"]

    def __str__(self) -> str:
        return self.committee_name


class AppealArbitration(models.Model):
    """申诉仲裁"""

    appeal = models.OneToOneField(
        Appeal, on_delete=models.CASCADE, related_name="arbitration", verbose_name="申诉"
    )
    committee = models.ForeignKey(
        ArbitrationCommittee,
        on_delete=models.RESTRICT,
        related_name="arbitrations",
        verbose_name="仲裁委员会",
    )
    arbitration_time = models.DateTimeField(null=True, blank=True, verbose_name="仲裁时间")
    arbitration_basis = models.TextField(null=True, blank=True, verbose_name="仲裁依据")
    arbitration_result = models.TextField(verbose_name="仲裁结果")
    public_time = models.DateTimeField(null=True, blank=True, verbose_name="公示时间")
    bay_arb_reference = models.CharField(max_length=255, null=True, blank=True, verbose_name="仲裁条例引用")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "申诉仲裁"
        verbose_name_plural = "申诉仲裁"
        ordering = ["-arbitration_time", "-create_time"]
        indexes = [
            models.Index(fields=["committee"], name="idx_arbitration_committee"),
        ]

    def __str__(self) -> str:
        return f"{self.appeal_id}-{self.committee}"
