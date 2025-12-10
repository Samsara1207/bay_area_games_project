from django.db import models


class Sponsor(models.Model):
    """赞助商"""

    SPONSOR_TYPE = (("现金", "现金"), ("物资", "物资"), ("服务", "服务"))

    sponsor_name = models.CharField(max_length=100, verbose_name="赞助商名称")
    sponsor_type = models.CharField(max_length=10, choices=SPONSOR_TYPE, verbose_name="赞助类型")
    sponsor_value = models.CharField(max_length=100, verbose_name="赞助金额/物资")
    coop_period = models.CharField(max_length=50, null=True, blank=True, verbose_name="合作期限")
    bay_register_address = models.CharField(max_length=255, null=True, blank=True, verbose_name="大湾区注册地址")
    contact_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="联系人")
    contact_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系电话")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "赞助商"
        verbose_name_plural = "赞助商"
        ordering = ["-create_time"]
        indexes = [models.Index(fields=["sponsor_type"], name="idx_sponsor_type")]

    def __str__(self) -> str:
        return self.sponsor_name


class SponsorRights(models.Model):
    """赞助商权益"""

    RIGHTS_TYPE = (("冠名", "冠名"), ("广告", "广告"), ("颁奖", "颁奖"), ("物料赞助", "物料赞助"))
    RIGHTS_STATUS = (("已执行", "已执行"), ("未执行", "未执行"), ("部分执行", "部分执行"))

    sponsor = models.ForeignKey(
        Sponsor, on_delete=models.CASCADE, related_name="rights", verbose_name="赞助商"
    )
    event = models.ForeignKey(
        "event_management.Event", on_delete=models.CASCADE, related_name="sponsor_rights", verbose_name="项目"
    )
    rights_type = models.CharField(max_length=10, choices=RIGHTS_TYPE, verbose_name="权益类型")
    rights_status = models.CharField(max_length=10, choices=RIGHTS_STATUS, default="未执行", verbose_name="执行状态")
    exposure_count = models.PositiveIntegerField(default=0, verbose_name="曝光次数")
    bay_media_channel = models.CharField(max_length=255, null=True, blank=True, verbose_name="媒体渠道")
    finance = models.ForeignKey(
        "finance_safety.Finance",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sponsor_rights",
        verbose_name="财务结算",
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "赞助商权益"
        verbose_name_plural = "赞助商权益"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["sponsor"], name="idx_rights_sponsor"),
            models.Index(fields=["event"], name="idx_rights_event"),
        ]

    def __str__(self) -> str:
        return f"{self.sponsor}-{self.rights_type}"


class AudienceTicket(models.Model):
    """观众票务"""

    PURCHASE_CHANNEL = (("大湾区线上", "大湾区线上"), ("大湾区线下", "大湾区线下"), ("其他", "其他"))
    REFUND_STATUS = (("未退票", "未退票"), ("已退票", "已退票"))
    NOTICE_STATUS = (("已确认", "已确认"), ("未确认", "未确认"))

    audience_name = models.CharField(max_length=50, verbose_name="观众姓名")
    audience_id_card = models.CharField(max_length=30, null=True, blank=True, verbose_name="证件号")
    event = models.ForeignKey(
        "event_management.Event", on_delete=models.RESTRICT, related_name="audience_tickets", verbose_name="项目"
    )
    seat_no = models.CharField(max_length=20, null=True, blank=True, verbose_name="座位号")
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name="票价")
    purchase_channel = models.CharField(max_length=10, choices=PURCHASE_CHANNEL, verbose_name="购票渠道")
    refund_status = models.CharField(max_length=5, choices=REFUND_STATUS, default="未退票", verbose_name="退票状态")
    entry_verification_code = models.CharField(max_length=50, null=True, blank=True, verbose_name="核验码")
    notice_confirm_status = models.CharField(
        max_length=5, choices=NOTICE_STATUS, default="未确认", verbose_name="观赛须知确认"
    )
    entry_time = models.DateTimeField(null=True, blank=True, verbose_name="入场时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "观众票务"
        verbose_name_plural = "观众票务"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["event"], name="idx_ticket_event"),
            models.Index(fields=["audience_id_card"], name="idx_ticket_idcard"),
        ]

    def __str__(self) -> str:
        return f"{self.audience_name}-{self.event}"
