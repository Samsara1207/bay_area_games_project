from django.db import models


class Team(models.Model):
    """代表队信息"""

    team_name = models.CharField(max_length=100, verbose_name="代表队名称")
    team_code = models.CharField(max_length=10, null=True, blank=True, verbose_name="代表队编码")
    sport_type = models.CharField(max_length=50, default="综合", verbose_name="运动类型")
    region = models.CharField(max_length=50, verbose_name="所属大湾区城市")
    city_code = models.CharField(max_length=6, verbose_name="城市编码")
    leader_name = models.CharField(max_length=50, verbose_name="领队姓名")
    leader_phone = models.CharField(max_length=20, verbose_name="领队电话")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    doctor_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="队医姓名")
    doctor_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="队医电话")
    logo_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="队徽地址")
    accommodation = models.CharField(max_length=255, null=True, blank=True, verbose_name="住宿信息")
    transport = models.CharField(max_length=255, null=True, blank=True, verbose_name="交通安排")
    uniform_custom = models.CharField(max_length=255, null=True, blank=True, verbose_name="队服定制信息")
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="经费预算")
    insurance_no = models.CharField(max_length=50, null=True, blank=True, verbose_name="保险单号")
    physical_report_url = models.URLField(max_length=255, null=True, blank=True, verbose_name="体检报告地址")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "代表队"
        verbose_name_plural = "代表队"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["region"], name="idx_team_region"),
            models.Index(fields=["city_code"], name="idx_team_city_code"),
        ]

    def __str__(self) -> str:
        return self.team_name


class Athlete(models.Model):
    """运动员信息"""

    GENDER_CHOICES = (
        ("男", "男"),
        ("女", "女"),
        ("其他", "其他"),
    )
    HUKOU_CHOICES = (
        ("广东", "广东"),
        ("香港", "香港"),
        ("澳门", "澳门"),
        ("其他", "其他"),
    )
    QUALIFICATION_CHOICES = (
        ("已审核", "已审核"),
        ("未审核", "未审核"),
        ("驳回", "驳回"),
    )
    DOPING_CHOICES = (
        ("合格", "合格"),
        ("不合格", "不合格"),
        ("待检测", "待检测"),
    )

    name = models.CharField(max_length=50, verbose_name="姓名")
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name="性别")
    birth_date = models.DateField(verbose_name="出生日期")
    id_card = models.CharField(max_length=30, null=True, blank=True, verbose_name="证件号")
    bay_area_hukou = models.CharField(max_length=10, choices=HUKOU_CHOICES, verbose_name="大湾区户籍")
    height = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="身高米")
    weight = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="体重公斤")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="联系电话")
    emergency_contact = models.CharField(max_length=50, null=True, blank=True, verbose_name="紧急联系人")
    emergency_phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="紧急联系电话")
    health_status = models.CharField(max_length=100, null=True, blank=True, verbose_name="健康状况")
    qualification_status = models.CharField(
        max_length=10, choices=QUALIFICATION_CHOICES, default="未审核", verbose_name="资格状态"
    )
    competition_id = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name="参赛证号")
    past_records = models.TextField(null=True, blank=True, verbose_name="过往参赛记录")
    doping_test = models.CharField(
        max_length=10, choices=DOPING_CHOICES, default="待检测", verbose_name="兴奋剂检测"
    )
    clothing_size = models.CharField(max_length=20, null=True, blank=True, verbose_name="服装尺码")
    insurance_info = models.CharField(max_length=255, null=True, blank=True, verbose_name="保险信息")
    # 关键修改：删除 Team 时级联删除 Athlete（CASCADE）
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name="athletes", verbose_name="所属代表队")
    join_time = models.DateTimeField(null=True, blank=True, verbose_name="入队时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "运动员"
        verbose_name_plural = "运动员"
        ordering = ["-create_time"]
        indexes = [
            models.Index(fields=["team"], name="idx_athlete_team"),
            models.Index(fields=["bay_area_hukou"], name="idx_athlete_hukou"),
            models.Index(fields=["qualification_status"], name="idx_athlete_qual"),
        ]

    def __str__(self) -> str:
        return self.name
