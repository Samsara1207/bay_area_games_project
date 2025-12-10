from django.db import models


class DataReport(models.Model):
    """数据统计报表"""

    REPORT_TYPE = (("日报", "日报"), ("周报", "周报"), ("总榜", "总榜"), ("专项", "专项"))
    EXPORT_STATUS = (("已导出", "已导出"), ("未导出", "未导出"))

    stat_dimension = models.CharField(max_length=50, verbose_name="统计维度")
    stat_indicator = models.CharField(max_length=100, verbose_name="统计指标")
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE, verbose_name="报表类型")
    stat_data = models.TextField(verbose_name="统计数据JSON")
    generate_time = models.DateTimeField(auto_now_add=True, verbose_name="生成时间")
    export_status = models.CharField(max_length=5, choices=EXPORT_STATUS, default="未导出", verbose_name="导出状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "数据统计报表"
        verbose_name_plural = "数据统计报表"
        ordering = ["-generate_time"]
        indexes = [
            models.Index(fields=["stat_dimension"], name="idx_report_dimension"),
            models.Index(fields=["report_type"], name="idx_report_type"),
            models.Index(fields=["generate_time"], name="idx_report_generate"),
        ]

    def __str__(self) -> str:
        return f"{self.report_type}-{self.stat_dimension}"
