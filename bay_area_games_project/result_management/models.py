from django.db import models


class Result(models.Model):
    """比赛成绩"""

    ROUND_CHOICES = (("预赛", "预赛"), ("复赛", "复赛"), ("决赛", "决赛"))
    YES_NO = (("是", "是"), ("否", "否"))
    RECORD_STATUS = (("已认证", "已认证"), ("未认证", "未认证"))

    apply = models.OneToOneField(
        "event_management.AthleteEvent", on_delete=models.CASCADE, related_name="result", verbose_name="报名"
    )
    result_value = models.CharField(max_length=50, verbose_name="成绩值")
    ranking = models.PositiveIntegerField(null=True, blank=True, verbose_name="排名")
    round = models.CharField(max_length=5, choices=ROUND_CHOICES, null=True, blank=True, verbose_name="轮次")
    is_record = models.CharField(max_length=2, choices=YES_NO, default="否", verbose_name="是否破纪录")
    wind_speed = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="风速")
    score = models.IntegerField(null=True, blank=True, verbose_name="得分")
    referee_scores = models.TextField(null=True, blank=True, verbose_name="裁判打分")
    video_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="视频回放")
    appeal = models.ForeignKey(
        "appeal_arbitration.Appeal", null=True, blank=True, on_delete=models.SET_NULL, related_name="results"
    )
    score_value = models.IntegerField(null=True, blank=True, verbose_name="积分值")
    record_cert_status = models.CharField(
        max_length=4, choices=RECORD_STATUS, default="未认证", verbose_name="破纪录认证"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "成绩"
        verbose_name_plural = "成绩"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["ranking"], name="idx_result_rank"),
            models.Index(fields=["is_record"], name="idx_result_record"),
        ]

    def __str__(self) -> str:
        return f"{self.apply_id}-{self.result_value}"


class MedalHonor(models.Model):
    """奖牌与荣誉"""

    MEDAL_TYPE = (
        ("金牌", "金牌"),
        ("银牌", "银牌"),
        ("铜牌", "铜牌"),
        ("集体奖", "集体奖"),
        ("道德风尚奖", "道德风尚奖"),
    )
    PUBLIC_STATUS = (("已公示", "已公示"), ("未公示", "未公示"))

    medal_type = models.CharField(max_length=20, choices=MEDAL_TYPE, verbose_name="奖牌类型")
    athlete = models.ForeignKey(
        "basic_info.Athlete", null=True, blank=True, on_delete=models.SET_NULL, related_name="medal_honors"
    )
    team = models.ForeignKey(
        "basic_info.Team", null=True, blank=True, on_delete=models.SET_NULL, related_name="medal_honors"
    )
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="medal_honors", verbose_name="成绩")
    award_guest = models.CharField(max_length=50, null=True, blank=True, verbose_name="颁奖嘉宾")
    honor_cert_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="证书编号")
    public_status = models.CharField(max_length=4, choices=PUBLIC_STATUS, default="未公示", verbose_name="公示状态")
    award_time = models.DateTimeField(null=True, blank=True, verbose_name="颁发时间")
    award_venue = models.CharField(max_length=100, null=True, blank=True, verbose_name="颁奖地点")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "奖牌与荣誉"
        verbose_name_plural = "奖牌与荣誉"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["athlete"], name="idx_medal_athlete"),
            models.Index(fields=["team"], name="idx_medal_team"),
            models.Index(fields=["result"], name="idx_medal_result"),
        ]

    def __str__(self) -> str:
        return f"{self.medal_type}-{self.result_id}"
