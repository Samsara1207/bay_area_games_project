from django.db import models


class Referee(models.Model):
    """裁判信息"""

    name = models.CharField(max_length=50, verbose_name="裁判姓名")
    gender = models.CharField(max_length=2, choices=(("男", "男"), ("女", "女"), ("其他", "其他")), verbose_name="性别")
    referee_level = models.CharField(
        max_length=20, choices=(("国家级", "国家级"), ("省级", "省级"), ("大湾区认证", "大湾区认证")), verbose_name="裁判等级"
    )
    charge_event = models.CharField(max_length=100, null=True, blank=True, verbose_name="负责项目")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系电话")
    bay_cert = models.CharField(max_length=5, choices=(("有", "有"), ("无", "无")), default="无", verbose_name="湾区认证")
    multi_language = models.CharField(max_length=50, null=True, blank=True, verbose_name="多语言能力")
    referee_history = models.TextField(null=True, blank=True, verbose_name="执裁历史")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "裁判"
        verbose_name_plural = "裁判"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["referee_level"], name="idx_referee_level"),
            models.Index(fields=["bay_cert"], name="idx_referee_cert"),
        ]

    def __str__(self) -> str:
        return self.name


class RefereeGroup(models.Model):
    """裁判组"""

    group_name = models.CharField(max_length=100, verbose_name="裁判组名称")
    leader_referee = models.ForeignKey(
        Referee, on_delete=models.SET_NULL, null=True, blank=True, related_name="lead_groups", verbose_name="组长"
    )
    event = models.ForeignKey(
        "event_management.Event", on_delete=models.CASCADE, related_name="referee_groups", verbose_name="负责项目"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "裁判组"
        verbose_name_plural = "裁判组"
        ordering = ["-create_time"]
        indexes = [models.Index(fields=["event"], name="idx_ref_group_event")]

    def __str__(self) -> str:
        return self.group_name


class RefereeArrangement(models.Model):
    """执裁安排"""

    CHECK_STATUS = (("已签到", "已签到"), ("未签到", "未签到"))

    referee_group = models.ForeignKey(
        RefereeGroup, on_delete=models.CASCADE, related_name="arrangements", verbose_name="裁判组"
    )
    referee = models.ForeignKey(
        Referee, on_delete=models.CASCADE, related_name="arrangements", verbose_name="裁判"
    )
    event = models.ForeignKey(
        "event_management.Event", on_delete=models.CASCADE, related_name="referee_arrangements", verbose_name="项目"
    )
    arrange_date = models.DateTimeField(verbose_name="执裁时间")
    position = models.CharField(max_length=50, null=True, blank=True, verbose_name="执裁岗位")
    check_in_status = models.CharField(
        max_length=5, choices=CHECK_STATUS, default="未签到", verbose_name="签到状态"
    )
    evaluation = models.CharField(max_length=255, null=True, blank=True, verbose_name="执裁评价")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "执裁安排"
        verbose_name_plural = "执裁安排"
        ordering = ["-arrange_date"]
        indexes = [
            models.Index(fields=["referee"], name="idx_arr_referee"),
            models.Index(fields=["event"], name="idx_arr_event"),
        ]

    def __str__(self) -> str:
        return f"{self.referee}-{self.event}-{self.arrange_date}"
