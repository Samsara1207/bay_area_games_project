from django.db import models


class Schedule(models.Model):
    """赛事日程"""

    STATUS = (("未开始", "未开始"), ("进行中", "进行中"), ("已结束", "已结束"))

    event = models.ForeignKey(
        "event_management.Event", on_delete=models.CASCADE, related_name="schedules", verbose_name="项目"
    )
    venue = models.ForeignKey(
        "event_management.Venue", on_delete=models.RESTRICT, related_name="schedules", verbose_name="场地"
    )
    schedule_date = models.DateField(verbose_name="日程日期")
    time_slot = models.CharField(max_length=50, verbose_name="时间段")
    status = models.CharField(max_length=5, choices=STATUS, default="未开始", verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "赛事日程"
        verbose_name_plural = "赛事日程"
        ordering = ["-schedule_date", "-time_slot"]
        indexes = [
            models.Index(fields=["event"], name="idx_schedule_event"),
            models.Index(fields=["venue"], name="idx_schedule_venue"),
            models.Index(fields=["schedule_date"], name="idx_schedule_date"),
        ]

    def __str__(self) -> str:
        return f"{self.event}-{self.schedule_date} {self.time_slot}"


class EventOperation(models.Model):
    """赛事运营环节"""

    OP_LINK = (("报名", "报名"), ("检录", "检录"), ("比赛", "比赛"), ("颁奖", "颁奖"), ("申诉", "申诉"))
    STATUS = (("未开始", "未开始"), ("进行中", "进行中"), ("已结束", "已结束"))
    APPROVAL = (("已审批", "已审批"), ("未审批", "未审批"))

    event = models.ForeignKey(
        "event_management.Event", on_delete=models.CASCADE, related_name="operations", verbose_name="项目"
    )
    operation_link = models.CharField(max_length=10, choices=OP_LINK, verbose_name="运营环节")
    status = models.CharField(max_length=5, choices=STATUS, default="未开始", verbose_name="状态")
    staff_id = models.PositiveIntegerField(null=True, blank=True, verbose_name="负责人编号")
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="开始时间")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="结束时间")
    exception_log = models.TextField(null=True, blank=True, verbose_name="异常日志")
    bay_approval_status = models.CharField(
        max_length=5, choices=APPROVAL, default="未审批", verbose_name="湾区审批状态"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "赛事运营"
        verbose_name_plural = "赛事运营"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["event"], name="idx_op_event"),
            models.Index(fields=["operation_link"], name="idx_op_link"),
        ]

    def __str__(self) -> str:
        return f"{self.event}-{self.operation_link}-{self.status}"
