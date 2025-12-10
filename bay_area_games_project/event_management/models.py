from django.db import models


class Venue(models.Model):
    """比赛场地"""

    venue_name = models.CharField(max_length=100, verbose_name="场地名称")
    capacity = models.PositiveIntegerField(null=True, blank=True, verbose_name="容纳人数")
    address = models.CharField(max_length=255, verbose_name="场地地址")
    facility_status = models.CharField(
        max_length=10,
        choices=(("正常", "正常"), ("维修中", "维修中"), ("停用", "停用")),
        default="正常",
        verbose_name="设施状态",
    )
    manager_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="负责人")
    manager_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="负责人电话")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "比赛场地"
        verbose_name_plural = "比赛场地"
        ordering = ["-create_time"]
        indexes = [models.Index(fields=["venue_name"], name="idx_venue_name")]

    def __str__(self) -> str:
        return self.venue_name


class Event(models.Model):
    """比赛项目"""

    event_name = models.CharField(max_length=100, verbose_name="项目名称")
    event_type = models.CharField(max_length=50, verbose_name="项目类型")
    gender_limit = models.CharField(
        max_length=2, choices=(("男", "男"), ("女", "女"), ("混合", "混合")), verbose_name="性别限制"
    )
    player_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name="参赛人数限制")
    event_time = models.DateTimeField(null=True, blank=True, verbose_name="比赛时间")
    venue = models.ForeignKey(Venue, on_delete=models.RESTRICT, related_name="events", verbose_name="场地")
    rule_doc_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="规则文档")
    apply_deadline = models.DateTimeField(null=True, blank=True, verbose_name="报名截止时间")
    referee_group = models.ForeignKey(
        "referee_management.RefereeGroup",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events",
        verbose_name="裁判组",
    )
    bay_feature = models.CharField(
        max_length=2, choices=(("是", "是"), ("否", "否")), default="否", verbose_name="湾区特色项目"
    )
    score_rule = models.TextField(null=True, blank=True, verbose_name="积分规则")
    live_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="直播地址")
    equipment_list = models.TextField(null=True, blank=True, verbose_name="器材清单")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "比赛项目"
        verbose_name_plural = "比赛项目"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["event_type"], name="idx_event_type"),
            models.Index(fields=["venue"], name="idx_event_venue"),
            models.Index(fields=["bay_feature"], name="idx_event_bay_feature"),
        ]

    def __str__(self) -> str:
        return self.event_name


class Group(models.Model):
    """赛事分组"""

    group_name = models.CharField(max_length=100, verbose_name="分组名称")
    age_range = models.CharField(max_length=50, null=True, blank=True, verbose_name="年龄范围")
    rule = models.TextField(null=True, blank=True, verbose_name="分组规则")
    disability_integration = models.CharField(
        max_length=2, choices=(("是", "是"), ("否", "否")), default="否", verbose_name="残健融合"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="groups", verbose_name="所属项目")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "赛事分组"
        verbose_name_plural = "赛事分组"
        ordering = ["-create_time"]
        indexes = [models.Index(fields=["event"], name="idx_group_event")]

    def __str__(self) -> str:
        return self.group_name


class AthleteEvent(models.Model):
    """运动员报名"""

    APPLY_STATUS = (("已报名", "已报名"), ("已取消", "已取消"), ("审核中", "审核中"))

    athlete = models.ForeignKey(
        "basic_info.Athlete", on_delete=models.CASCADE, related_name="athlete_events", verbose_name="运动员"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="athlete_events", verbose_name="项目")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="athlete_events", verbose_name="分组")
    apply_time = models.DateTimeField(auto_now_add=True, verbose_name="报名时间")
    apply_status = models.CharField(max_length=10, choices=APPLY_STATUS, default="审核中", verbose_name="报名状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "运动员报名"
        verbose_name_plural = "运动员报名"
        ordering = ["-apply_time"]
        unique_together = ("athlete", "event", "group")
        indexes = [
            models.Index(fields=["athlete"], name="idx_ae_athlete"),
            models.Index(fields=["event"], name="idx_ae_event"),
        ]

    def __str__(self) -> str:
        return f"{self.athlete}-{self.event}-{self.group}"
