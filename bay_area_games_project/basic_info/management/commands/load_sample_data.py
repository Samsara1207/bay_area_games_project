import json
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from appeal_arbitration.models import Appeal, AppealArbitration, ArbitrationCommittee
from basic_info.models import Athlete, Team
from business.models import AudienceTicket, Sponsor, SponsorRights
from data_statistics.models import DataReport
from event_management.models import AthleteEvent, Event, Group, Venue
from finance_safety.models import EpidemicSafety, Finance
from logistics.models import LogisticsDetail, Supplier, Volunteer
from operation.models import EventOperation, Schedule
from referee_management.models import Referee, RefereeArrangement, RefereeGroup
from result_management.models import MedalHonor, Result


def dt(value: str):
    return datetime.fromisoformat(value)


class Command(BaseCommand):
    help = "导入示例数据到本地 SQLite（幂等，按唯一字段查找）"

    @transaction.atomic
    def handle(self, *args, **options):
        self.load_basic()
        self.load_events()
        self.load_referees()
        self.load_results()
        self.load_logistics()
        self.load_operation()
        self.load_appeal()
        self.load_business()
        self.load_finance_safety()
        self.load_statistics()
        self.stdout.write(self.style.SUCCESS("示例数据导入完成"))

    def load_basic(self):
        teams_data = [
            {
                "team_name": "广东省广州市代表队",
                "region": "广州",
                "city_code": "01",
                "leader_name": "张三",
                "leader_phone": "13800138000",
                "doctor_name": "李四",
                "doctor_phone": "13900139000",
                "uniform_custom": "短袖套装，红色主色调",
                "budget": 500000.00,
                "insurance_no": "INS-GZ-2025001",
                "physical_report_url": "https://example.com/report/gz001.pdf",
            },
            {
                "team_name": "中国香港代表队",
                "region": "香港",
                "city_code": "03",
                "leader_name": "王五",
                "leader_phone": "13700137000",
                "doctor_name": "赵六",
                "doctor_phone": "13600136000",
                "uniform_custom": "长袖套装，紫荆花标识",
                "budget": 800000.00,
                "insurance_no": "INS-HK-2025001",
                "physical_report_url": "https://example.com/report/hk001.pdf",
            },
            {
                "team_name": "中国澳门代表队",
                "region": "澳门",
                "city_code": "04",
                "leader_name": "钱七",
                "leader_phone": "13500135000",
                "doctor_name": "孙八",
                "doctor_phone": "13400134000",
                "uniform_custom": "短袖套装，莲花标识",
                "budget": 600000.00,
                "insurance_no": "INS-MO-2025001",
                "physical_report_url": "https://example.com/report/mo001.pdf",
            },
        ]
        teams = []
        for data in teams_data:
            obj, _ = Team.objects.update_or_create(team_name=data["team_name"], defaults=data)
            teams.append(obj)

        athletes_data = [
            {
                "name": "李小华",
                "gender": "男",
                "birth_date": datetime(1998, 5, 10).date(),
                "id_card": "440101199805101234",
                "bay_area_hukou": "广东",
                "height": 1.80,
                "weight": 75.0,
                "phone": "13812345678",
                "emergency_contact": "李父",
                "emergency_phone": "13887654321",
                "health_status": "健康",
                "qualification_status": "已审核",
                "competition_id": "ATH-GZ-2025001",
                "doping_test": "合格",
                "clothing_size": "XL",
                "insurance_info": "意外险+医疗险，承保公司：平安",
                "team": teams[0],
                "join_time": dt("2025-01-01 00:00:00"),
            },
            {
                "name": "陈志强",
                "gender": "男",
                "birth_date": datetime(1999, 8, 15).date(),
                "id_card": "H1234567890",
                "bay_area_hukou": "香港",
                "height": 1.78,
                "weight": 72.5,
                "phone": "13912345678",
                "emergency_contact": "陈母",
                "emergency_phone": "13987654321",
                "health_status": "健康",
                "qualification_status": "已审核",
                "competition_id": "ATH-HK-2025001",
                "doping_test": "合格",
                "clothing_size": "L",
                "insurance_info": "跨境保险，承保公司：友邦",
                "team": teams[1],
                "join_time": dt("2025-01-05 00:00:00"),
            },
            {
                "name": "林美琪",
                "gender": "女",
                "birth_date": datetime(2000, 3, 20).date(),
                "id_card": "M0987654321",
                "bay_area_hukou": "澳门",
                "height": 1.65,
                "weight": 55.0,
                "phone": "13712345678",
                "emergency_contact": "林父",
                "emergency_phone": "13787654321",
                "health_status": "健康",
                "qualification_status": "已审核",
                "competition_id": "ATH-MO-2025001",
                "doping_test": "合格",
                "clothing_size": "M",
                "insurance_info": "跨境保险，承保公司：太平",
                "team": teams[2],
                "join_time": dt("2025-01-10 00:00:00"),
            },
        ]
        for data in athletes_data:
            Athlete.objects.update_or_create(competition_id=data["competition_id"], defaults=data)

    def load_events(self):
        venues_data = [
            {
                "venue_name": "广州奥体中心",
                "capacity": 50000,
                "address": "广州市天河区奥体南路12号",
                "facility_status": "正常",
                "manager_name": "周经理",
                "manager_phone": "13800138001",
            },
            {
                "venue_name": "香港维多利亚公园体育馆",
                "capacity": 10000,
                "address": "香港湾仔区铜锣湾高士威道",
                "facility_status": "正常",
                "manager_name": "陈经理",
                "manager_phone": "13800138002",
            },
            {
                "venue_name": "澳门塔石体育馆",
                "capacity": 8000,
                "address": "澳门花地玛堂区士多鸟拜斯大马路",
                "facility_status": "正常",
                "manager_name": "李经理",
                "manager_phone": "13800138003",
            },
        ]
        venues = []
        for data in venues_data:
            obj, _ = Venue.objects.update_or_create(venue_name=data["venue_name"], defaults=data)
            venues.append(obj)

        events_data = [
            {
                "event_name": "男子500米龙舟",
                "event_type": "大湾区传统项目",
                "gender_limit": "男",
                "player_limit": 20,
                "event_time": dt("2025-06-10 09:00:00"),
                "venue": venues[0],
                "rule_doc_url": "https://example.com/rule/dragonboat.pdf",
                "apply_deadline": dt("2025-05-20 23:59:59"),
                "referee_group": None,
                "bay_feature": "是",
                "score_rule": "第一名积10分，第二名8分，第三名6分",
                "live_url": "https://live.baygames.com/dragonboat",
                "equipment_list": "龙舟10艘、救生衣200件、鼓10面",
            },
            {
                "event_name": "男子100米短跑",
                "event_type": "田径",
                "gender_limit": "男",
                "player_limit": 100,
                "event_time": dt("2025-06-11 10:00:00"),
                "venue": venues[0],
                "rule_doc_url": "https://example.com/rule/100m.pdf",
                "apply_deadline": dt("2025-05-20 23:59:59"),
                "referee_group": None,
                "bay_feature": "否",
                "score_rule": "按成绩排名，破纪录额外加2分",
                "live_url": "https://live.baygames.com/100m",
                "equipment_list": "起跑器10组、计时设备5套",
            },
            {
                "event_name": "港澳特邀组羽毛球单打",
                "event_type": "球类",
                "gender_limit": "混合",
                "player_limit": 50,
                "event_time": dt("2025-06-12 14:00:00"),
                "venue": venues[1],
                "rule_doc_url": "https://example.com/rule/badminton.pdf",
                "apply_deadline": dt("2025-05-20 23:59:59"),
                "referee_group": None,
                "bay_feature": "否",
                "score_rule": "三局两胜制，每局21分",
                "live_url": "https://live.baygames.com/badminton",
                "equipment_list": "羽毛球拍50支、羽毛球100筒",
            },
        ]
        events = []
        for data in events_data:
            obj, _ = Event.objects.update_or_create(event_name=data["event_name"], defaults=data)
            events.append(obj)

        groups_data = [
            {"group_name": "龙舟成年组", "age_range": "18-45岁", "rule": "无残健融合，纯成年组", "disability_integration": "否", "event": events[0]},
            {"group_name": "100米短跑青年组", "age_range": "18-25岁", "rule": "青年组，无残健融合", "disability_integration": "否", "event": events[1]},
            {"group_name": "港澳特邀组羽毛球", "age_range": "18-50岁", "rule": "仅限港澳籍运动员，残健融合", "disability_integration": "是", "event": events[2]},
        ]
        groups = []
        for data in groups_data:
            obj, _ = Group.objects.update_or_create(group_name=data["group_name"], defaults=data)
            groups.append(obj)

        athletes = list(Athlete.objects.all().order_by("id"))
        apply_data = [
            {"athlete": athletes[0], "event": events[0], "group": groups[0], "apply_time": dt("2025-05-10 10:00:00"), "apply_status": "已报名"},
            {"athlete": athletes[1], "event": events[1], "group": groups[1], "apply_time": dt("2025-05-11 10:00:00"), "apply_status": "已报名"},
            {"athlete": athletes[2], "event": events[2], "group": groups[2], "apply_time": dt("2025-05-12 10:00:00"), "apply_status": "已报名"},
        ]
        for data in apply_data:
            AthleteEvent.objects.update_or_create(
                athlete=data["athlete"], event=data["event"], group=data["group"], defaults=data
            )

    def load_referees(self):
        refs_data = [
            {
                "name": "黄裁判",
                "gender": "男",
                "referee_level": "大湾区认证",
                "charge_event": "龙舟",
                "phone": "13811112222",
                "bay_cert": "有",
                "multi_language": "中/粤/英",
                "referee_history": "2024大湾区龙舟赛执裁、2023大湾区运动会执裁",
            },
            {
                "name": "张裁判",
                "gender": "女",
                "referee_level": "国家级",
                "charge_event": "100米短跑",
                "phone": "13833334444",
                "bay_cert": "有",
                "multi_language": "中/英",
                "referee_history": "2024全国田径锦标赛执裁、2025大湾区运动会执裁",
            },
            {
                "name": "李裁判",
                "gender": "男",
                "referee_level": "大湾区认证",
                "charge_event": "羽毛球",
                "phone": "13855556666",
                "bay_cert": "有",
                "multi_language": "中/粤/葡",
                "referee_history": "2024澳门羽毛球公开赛执裁、2025大湾区运动会执裁",
            },
        ]
        refs = []
        for data in refs_data:
            obj, _ = Referee.objects.update_or_create(name=data["name"], defaults=data)
            refs.append(obj)

        events = list(Event.objects.order_by("id"))
        groups_data = [
            {"group_name": "龙舟裁判组", "leader_referee": refs[0], "event": events[0]},
            {"group_name": "100米短跑裁判组", "leader_referee": refs[1], "event": events[1]},
            {"group_name": "羽毛球裁判组", "leader_referee": refs[2], "event": events[2]},
        ]
        rgs = []
        for data in groups_data:
            obj, _ = RefereeGroup.objects.update_or_create(group_name=data["group_name"], defaults=data)
            rgs.append(obj)

        arrangements = [
            {
                "referee_group": rgs[0],
                "referee": refs[0],
                "event": events[0],
                "arrange_date": dt("2025-06-10 08:00:00"),
                "position": "主裁",
                "check_in_status": "已签到",
                "evaluation": "执裁规范，无争议",
            },
            {
                "referee_group": rgs[1],
                "referee": refs[1],
                "event": events[1],
                "arrange_date": dt("2025-06-11 09:00:00"),
                "position": "主裁",
                "check_in_status": "已签到",
                "evaluation": "计时准确，判罚公正",
            },
            {
                "referee_group": rgs[2],
                "referee": refs[2],
                "event": events[2],
                "arrange_date": dt("2025-06-12 13:00:00"),
                "position": "主裁",
                "check_in_status": "已签到",
                "evaluation": "规则掌握熟练，多语言沟通顺畅",
            },
        ]
        for data in arrangements:
            RefereeArrangement.objects.update_or_create(
                referee_group=data["referee_group"],
                referee=data["referee"],
                event=data["event"],
                arrange_date=data["arrange_date"],
                defaults=data,
            )

    def load_results(self):
        applies = list(AthleteEvent.objects.order_by("id"))
        results = [
            {
                "apply": applies[0],
                "result_value": "1分50秒",
                "ranking": 1,
                "round": "决赛",
                "is_record": "是",
                "wind_speed": 0.5,
                "score": None,
                "referee_scores": "9.8,9.9,9.8",
                "video_url": "https://example.com/video/dragonboat001.mp4",
                "appeal": None,
                "score_value": 10,
                "record_cert_status": "已认证",
            },
            {
                "apply": applies[1],
                "result_value": "10.2秒",
                "ranking": 2,
                "round": "决赛",
                "is_record": "否",
                "wind_speed": 0.2,
                "score": None,
                "referee_scores": None,
                "video_url": "https://example.com/video/100m001.mp4",
                "appeal": None,
                "score_value": 8,
                "record_cert_status": "未认证",
            },
            {
                "apply": applies[2],
                "result_value": "21:18,21:16",
                "ranking": 1,
                "round": "决赛",
                "is_record": "否",
                "wind_speed": None,
                "score": 2,
                "referee_scores": "9.7,9.8,9.6",
                "video_url": "https://example.com/video/badminton001.mp4",
                "appeal": None,
                "score_value": 10,
                "record_cert_status": "未认证",
            },
        ]
        result_objs = []
        for data in results:
            obj, _ = Result.objects.update_or_create(apply=data["apply"], defaults=data)
            result_objs.append(obj)

        athletes = list(Athlete.objects.order_by("id"))
        teams = list(Team.objects.order_by("id"))
        honors = [
            {
                "medal_type": "金牌",
                "athlete": athletes[0],
                "team": teams[0],
                "result": result_objs[0],
                "award_guest": "广东省体育局局长",
                "honor_cert_no": "MED-GZ-2025001",
                "public_status": "已公示",
                "award_time": dt("2025-06-10 11:00:00"),
                "award_venue": "广州奥体中心",
            },
            {
                "medal_type": "银牌",
                "athlete": athletes[1],
                "team": teams[1],
                "result": result_objs[1],
                "award_guest": "香港体育协会主席",
                "honor_cert_no": "MED-HK-2025001",
                "public_status": "已公示",
                "award_time": dt("2025-06-11 12:00:00"),
                "award_venue": "广州奥体中心",
            },
            {
                "medal_type": "金牌",
                "athlete": athletes[2],
                "team": teams[2],
                "result": result_objs[2],
                "award_guest": "澳门体育局局长",
                "honor_cert_no": "MED-MO-2025001",
                "public_status": "已公示",
                "award_time": dt("2025-06-12 16:00:00"),
                "award_venue": "香港维多利亚公园体育馆",
            },
        ]
        for data in honors:
            MedalHonor.objects.update_or_create(
                honor_cert_no=data["honor_cert_no"], defaults=data
            )

    def load_logistics(self):
        suppliers_data = [
            {
                "supplier_name": "广州餐饮服务有限公司",
                "service_type": "餐饮",
                "bay_register_address": "广州市天河区天河路100号",
                "qualification_url": "https://example.com/qual/catering.pdf",
                "coop_period": "2025-01-01至2025-12-31",
                "contact_name": "王经理",
                "contact_phone": "13866667777",
                "performance_score": 4.8,
            },
            {
                "supplier_name": "香港交通服务有限公司",
                "service_type": "交通",
                "bay_register_address": "香港九龙尖沙咀弥敦道100号",
                "qualification_url": "https://example.com/qual/transport.pdf",
                "coop_period": "2025-01-01至2025-12-31",
                "contact_name": "陈经理",
                "contact_phone": "13888889999",
                "performance_score": 4.9,
            },
            {
                "supplier_name": "澳门器材租赁有限公司",
                "service_type": "器材",
                "bay_register_address": "澳门半岛新马路100号",
                "qualification_url": "https://example.com/qual/equipment.pdf",
                "coop_period": "2025-01-01至2025-12-31",
                "contact_name": "李经理",
                "contact_phone": "13899990000",
                "performance_score": 4.7,
            },
        ]
        suppliers = []
        for data in suppliers_data:
            obj, _ = Supplier.objects.update_or_create(supplier_name=data["supplier_name"], defaults=data)
            suppliers.append(obj)

        logistics_data = [
            {
                "service_type": "餐饮",
                "service_object_type": "运动员",
                "service_object_id": 1,
                "supplier": suppliers[0],
                "service_no": "LOG-CAT-2025001",
                "cost_amount": 500.00,
                "service_time": dt("2025-06-10 12:00:00"),
                "staff_name": "张厨师",
                "satisfaction_score": 5,
                "exception_record": "无",
            },
            {
                "service_type": "交通",
                "service_object_type": "运动员",
                "service_object_id": 2,
                "supplier": suppliers[1],
                "service_no": "LOG-TRA-2025001",
                "cost_amount": 1000.00,
                "service_time": dt("2025-06-11 08:00:00"),
                "staff_name": "陈司机",
                "satisfaction_score": 4,
                "exception_record": "轻微晚点10分钟",
            },
            {
                "service_type": "器材",
                "service_object_type": "运动员",
                "service_object_id": 3,
                "supplier": suppliers[2],
                "service_no": "LOG-EQP-2025001",
                "cost_amount": 2000.00,
                "service_time": dt("2025-06-12 10:00:00"),
                "staff_name": "李技术员",
                "satisfaction_score": 5,
                "exception_record": "无",
            },
        ]
        for data in logistics_data:
            LogisticsDetail.objects.update_or_create(service_no=data["service_no"], defaults=data)

        volunteers_data = [
            {
                "name": "王同学",
                "gender": "女",
                "bay_school_company": "中山大学",
                "service_post": "引导",
                "service_time_slot": "2025-06-10 08:00-18:00",
                "training_status": "已培训",
                "working_hours": 10.0,
                "evaluation": "服务热情，指引准确",
                "phone": "13811111111",
            },
            {
                "name": "陈同学",
                "gender": "男",
                "bay_school_company": "香港大学",
                "service_post": "检录",
                "service_time_slot": "2025-06-11 08:00-18:00",
                "training_status": "已培训",
                "working_hours": 10.0,
                "evaluation": "检录高效，无差错",
                "phone": "13822222222",
            },
            {
                "name": "林同学",
                "gender": "女",
                "bay_school_company": "澳门大学",
                "service_post": "医疗辅助",
                "service_time_slot": "2025-06-12 08:00-18:00",
                "training_status": "已培训",
                "working_hours": 10.0,
                "evaluation": "应急处理及时",
                "phone": "13833333333",
            },
        ]
        for data in volunteers_data:
            Volunteer.objects.update_or_create(name=data["name"], service_post=data["service_post"], defaults=data)

    def load_operation(self):
        events = list(Event.objects.order_by("id"))
        venues = list(Venue.objects.order_by("id"))
        schedules = [
            {"event": events[0], "venue": venues[0], "schedule_date": datetime(2025, 6, 10).date(), "time_slot": "09:00-11:00", "status": "已结束"},
            {"event": events[1], "venue": venues[0], "schedule_date": datetime(2025, 6, 11).date(), "time_slot": "10:00-12:00", "status": "已结束"},
            {"event": events[2], "venue": venues[1], "schedule_date": datetime(2025, 6, 12).date(), "time_slot": "14:00-16:00", "status": "已结束"},
        ]
        for data in schedules:
            Schedule.objects.update_or_create(event=data["event"], venue=data["venue"], schedule_date=data["schedule_date"], defaults=data)

        operations = [
            {"event": events[0], "operation_link": "比赛", "status": "已结束", "staff_id": None, "start_time": dt("2025-06-10 09:00:00"), "end_time": dt("2025-06-10 11:00:00"), "exception_log": "无", "bay_approval_status": "已审批"},
            {"event": events[1], "operation_link": "比赛", "status": "已结束", "staff_id": None, "start_time": dt("2025-06-11 10:00:00"), "end_time": dt("2025-06-11 12:00:00"), "exception_log": "无", "bay_approval_status": "已审批"},
            {"event": events[2], "operation_link": "比赛", "status": "已结束", "staff_id": None, "start_time": dt("2025-06-12 14:00:00"), "end_time": dt("2025-06-12 16:00:00"), "exception_log": "无", "bay_approval_status": "已审批"},
        ]
        for data in operations:
            EventOperation.objects.update_or_create(
                event=data["event"], operation_link=data["operation_link"], defaults=data
            )

    def load_appeal(self):
        athletes = list(Athlete.objects.order_by("id"))
        events = list(Event.objects.order_by("id"))
        appeal, _ = Appeal.objects.update_or_create(
            athlete=athletes[1],
            event=events[1],
            defaults={
                "appeal_content": "认为100米短跑成绩计时有误，申请复核（英文：I think the timing of the 100m sprint result is incorrect, apply for review）",
                "submit_time": dt("2025-06-11 13:00:00"),
                "status": "已解决",
                "result": "复核后成绩无误，维持原判",
                "handler_id": None,
            },
        )
        committee, _ = ArbitrationCommittee.objects.update_or_create(
            committee_name="大湾区体育仲裁委员会",
            defaults={
                "member_ids": "1,2,3",
                "scope": "负责大湾区运动会所有申诉仲裁",
                "contact_phone": "13800138004",
                "arbitration_process_url": "https://example.com/process/arbitration.pdf",
            },
        )
        AppealArbitration.objects.update_or_create(
            appeal=appeal,
            defaults={
                "committee": committee,
                "arbitration_time": dt("2025-06-11 15:00:00"),
                "arbitration_basis": "《大湾区体育赛事仲裁规则》第10条",
                "arbitration_result": "维持原判，成绩无误",
                "public_time": dt("2025-06-12 00:00:00"),
                "bay_arb_reference": "《大湾区体育仲裁条例》2025版第5章第8条",
            },
        )

    def load_business(self):
        sponsors_data = [
            {
                "sponsor_name": "广东某体育品牌",
                "sponsor_type": "现金",
                "sponsor_value": "500万元",
                "coop_period": "2025-01-01至2025-12-31",
                "bay_register_address": "广州市海珠区滨江路100号",
                "contact_name": "赵经理",
                "contact_phone": "13844445555",
            },
            {
                "sponsor_name": "香港某集团",
                "sponsor_type": "物资",
                "sponsor_value": "1000件运动服",
                "coop_period": "2025-01-01至2025-12-31",
                "bay_register_address": "香港中环皇后大道中100号",
                "contact_name": "钱经理",
                "contact_phone": "13855556666",
            },
            {
                "sponsor_name": "澳门某酒店",
                "sponsor_type": "服务",
                "sponsor_value": "100间免费客房",
                "coop_period": "2025-01-01至2025-12-31",
                "bay_register_address": "澳门路氹城金光大道100号",
                "contact_name": "孙经理",
                "contact_phone": "13866667777",
            },
        ]
        sponsors = []
        for data in sponsors_data:
            obj, _ = Sponsor.objects.update_or_create(sponsor_name=data["sponsor_name"], defaults=data)
            sponsors.append(obj)

        events = list(Event.objects.order_by("id"))
        rights = [
            {
                "sponsor": sponsors[0],
                "event": events[0],
                "rights_type": "冠名",
                "rights_status": "已执行",
                "exposure_count": 100000,
                "bay_media_channel": "广东卫视、大湾区卫视、南方都市报",
            },
            {
                "sponsor": sponsors[1],
                "event": events[1],
                "rights_type": "广告",
                "rights_status": "已执行",
                "exposure_count": 80000,
                "bay_media_channel": "香港TVB、香港商报",
            },
            {
                "sponsor": sponsors[2],
                "event": events[2],
                "rights_type": "物料赞助",
                "rights_status": "已执行",
                "exposure_count": 50000,
                "bay_media_channel": "澳门日报、澳广视",
            },
        ]
        for data in rights:
            SponsorRights.objects.update_or_create(
                sponsor=data["sponsor"], event=data["event"], rights_type=data["rights_type"], defaults=data
            )

        tickets = [
            {
                "audience_name": "刘观众",
                "audience_id_card": "440101199001011234",
                "event": events[0],
                "seat_no": "A1-01",
                "ticket_price": 200.00,
                "purchase_channel": "大湾区线上",
                "refund_status": "未退票",
                "entry_verification_code": "VER-GZ-2025001",
                "notice_confirm_status": "已确认",
                "entry_time": dt("2025-06-10 08:30:00"),
            },
            {
                "audience_name": "陈观众",
                "audience_id_card": "H1234567891",
                "event": events[1],
                "seat_no": "B2-02",
                "ticket_price": 300.00,
                "purchase_channel": "大湾区线下",
                "refund_status": "未退票",
                "entry_verification_code": "VER-HK-2025001",
                "notice_confirm_status": "已确认",
                "entry_time": dt("2025-06-11 09:30:00"),
            },
            {
                "audience_name": "李观众",
                "audience_id_card": "M0987654322",
                "event": events[2],
                "seat_no": "C3-03",
                "ticket_price": 250.00,
                "purchase_channel": "大湾区线上",
                "refund_status": "未退票",
                "entry_verification_code": "VER-MO-2025001",
                "notice_confirm_status": "已确认",
                "entry_time": dt("2025-06-12 13:30:00"),
            },
        ]
        for data in tickets:
            AudienceTicket.objects.update_or_create(
                audience_name=data["audience_name"], event=data["event"], seat_no=data["seat_no"], defaults=data
            )

    def load_finance_safety(self):
        finances = [
            {"finance_type": "报名费", "amount": 200.00, "related_no": "apply_id_1", "payer_payee": "李小华", "settle_status": "已结算", "bay_tax_record_no": "TAX-GZ-2025001"},
            {"finance_type": "赞助费", "amount": 5000000.00, "related_no": "sponsor_id_1", "payer_payee": "广东某体育品牌", "settle_status": "已结算", "bay_tax_record_no": "TAX-GZ-2025002"},
            {"finance_type": "后勤费", "amount": 500.00, "related_no": "logistics_id_1", "payer_payee": "广州餐饮服务有限公司", "settle_status": "已结算", "bay_tax_record_no": "TAX-GZ-2025003"},
            {"finance_type": "奖金", "amount": 10000.00, "related_no": "medal_honor_id_1", "payer_payee": "李小华", "settle_status": "已结算", "bay_tax_record_no": "TAX-GZ-2025004"},
        ]
        for data in finances:
            Finance.objects.update_or_create(related_no=data["related_no"], defaults=data)

        es_data = [
            {"person_type": "运动员", "person_id": 1, "temperature": 36.5, "safety_training_status": "已培训", "emergency_record": "无"},
            {"person_type": "运动员", "person_id": 2, "temperature": 36.6, "safety_training_status": "已培训", "emergency_record": "无"},
            {"person_type": "观众", "person_id": 1, "temperature": 36.4, "safety_training_status": "未培训", "emergency_record": "无"},
        ]
        for data in es_data:
            EpidemicSafety.objects.update_or_create(
                person_type=data["person_type"], person_id=data["person_id"], defaults=data
            )

    def load_statistics(self):
        reports = [
            {
                "stat_dimension": "大湾区城市",
                "stat_indicator": "参赛人数、奖牌数",
                "report_type": "总榜",
                "stat_data": json.dumps({"广州": {"参赛人数": 100, "金牌数": 10}, "香港": {"参赛人数": 80, "金牌数": 8}, "澳门": {"参赛人数": 60, "金牌数": 6}}, ensure_ascii=False),
                "generate_time": dt("2025-06-15 00:00:00"),
                "export_status": "已导出",
            },
            {
                "stat_dimension": "项目",
                "stat_indicator": "成绩、破纪录数",
                "report_type": "周报",
                "stat_data": json.dumps({"龙舟": {"最好成绩": "1分50秒", "破纪录数": 1}, "100米短跑": {"最好成绩": "10.1秒", "破纪录数": 0}}, ensure_ascii=False),
                "generate_time": dt("2025-06-14 00:00:00"),
                "export_status": "未导出",
            },
            {
                "stat_dimension": "代表队",
                "stat_indicator": "积分、获奖数",
                "report_type": "日报",
                "stat_data": json.dumps({"广东省广州市代表队": {"积分": 100, "获奖数": 15}, "中国香港代表队": {"积分": 80, "获奖数": 10}}, ensure_ascii=False),
                "generate_time": dt("2025-06-13 00:00:00"),
                "export_status": "已导出",
            },
        ]
        for data in reports:
            DataReport.objects.update_or_create(
                stat_dimension=data["stat_dimension"], report_type=data["report_type"], stat_indicator=data["stat_indicator"], defaults=data
            )

