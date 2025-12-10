USE bay_area_games;

-- ===================== 基础信息模块 =====================
-- 1. 代表队表（team）
INSERT INTO team (team_name, region, city_code, leader_name, leader_phone, doctor_name, doctor_phone, uniform_custom, budget, insurance_no, physical_report_url)
VALUES 
('广东省广州市代表队', '广州', '01', '张三', '13800138000', '李四', '13900139000', '短袖套装，红色主色调', 500000.00, 'INS-GZ-2025001', 'https://example.com/report/gz001.pdf'),
('中国香港代表队', '香港', '03', '王五', '13700137000', '赵六', '13600136000', '长袖套装，紫荆花标识', 800000.00, 'INS-HK-2025001', 'https://example.com/report/hk001.pdf'),
('中国澳门代表队', '澳门', '04', '钱七', '13500135000', '孙八', '13400134000', '短袖套装，莲花标识', 600000.00, 'INS-MO-2025001', 'https://example.com/report/mo001.pdf');

-- 2. 运动员表（athlete）
INSERT INTO athlete (name, gender, birth_date, id_card, bay_area_hukou, height, weight, phone, emergency_contact, emergency_phone, health_status, qualification_status, competition_id, doping_test, clothing_size, insurance_info, team_id, join_time)
VALUES 
-- 广东籍运动员
('李小华', '男', '1998-05-10', '440101199805101234', '广东', 1.80, 75.0, '13812345678', '李父', '13887654321', '健康', '已审核', 'ATH-GZ-2025001', '合格', 'XL', '意外险+医疗险，承保公司：平安', 1, '2025-01-01 00:00:00'),
-- 香港籍运动员
('陈志强', '男', '1999-08-15', 'H1234567890', '香港', 1.78, 72.5, '13912345678', '陈母', '13987654321', '健康', '已审核', 'ATH-HK-2025001', '合格', 'L', '跨境保险，承保公司：友邦', 2, '2025-01-05 00:00:00'),
-- 澳门籍运动员
('林美琪', '女', '2000-03-20', 'M0987654321', '澳门', 1.65, 55.0, '13712345678', '林父', '13787654321', '健康', '已审核', 'ATH-MO-2025001', '合格', 'M', '跨境保险，承保公司：太平', 3, '2025-01-10 00:00:00');

-- ===================== 赛事项目模块 =====================
-- 3. 场地表（venue）
INSERT INTO venue (venue_name, capacity, address, facility_status, manager_name, manager_phone)
VALUES 
('广州奥体中心', 50000, '广州市天河区奥体南路12号', '正常', '周经理', '13800138001'),
('香港维多利亚公园体育馆', 10000, '香港湾仔区铜锣湾高士威道', '正常', '陈经理', '13800138002'),
('澳门塔石体育馆', 8000, '澳门花地玛堂区士多鸟拜斯大马路', '正常', '李经理', '13800138003');

-- 4. 比赛项目表（event）
INSERT INTO event (event_name, event_type, gender_limit, player_limit, event_time, venue_id, rule_doc_url, apply_deadline, referee_group_id, bay_feature, score_rule, live_url, equipment_list)
VALUES 
-- 大湾区特色项目：龙舟
('男子500米龙舟', '大湾区传统项目', '男', 20, '2025-06-10 09:00:00', 1, 'https://example.com/rule/dragonboat.pdf', '2025-05-20 23:59:59', NULL, '是', '第一名积10分，第二名8分，第三名6分', 'https://live.baygames.com/dragonboat', '龙舟10艘、救生衣200件、鼓10面'),
-- 常规项目：100米短跑
('男子100米短跑', '田径', '男', 100, '2025-06-11 10:00:00', 1, 'https://example.com/rule/100m.pdf', '2025-05-20 23:59:59', NULL, '否', '按成绩排名，破纪录额外加2分', 'https://live.baygames.com/100m', '起跑器10组、计时设备5套'),
-- 港澳特邀组项目：羽毛球单打
('港澳特邀组羽毛球单打', '球类', '混合', 50, '2025-06-12 14:00:00', 2, 'https://example.com/rule/badminton.pdf', '2025-05-20 23:59:59', NULL, '否', '三局两胜制，每局21分', 'https://live.baygames.com/badminton', '羽毛球拍50支、羽毛球100筒');

-- 5. 赛事分组表（group）
INSERT INTO `group` (group_name, age_range, rule, disability_integration, event_id)
VALUES 
('龙舟成年组', '18-45岁', '无残健融合，纯成年组', '否', 1),
('100米短跑青年组', '18-25岁', '青年组，无残健融合', '否', 2),
('港澳特邀组羽毛球', '18-50岁', '仅限港澳籍运动员，残健融合', '是', 3);

-- 6. 运动员项目报名表（athlete_event）
INSERT INTO athlete_event (athlete_id, event_id, group_id, apply_time, apply_status)
VALUES 
(1, 1, 1, '2025-05-10 10:00:00', '已报名'),  -- 广东运动员报龙舟成年组
(2, 2, 2, '2025-05-11 10:00:00', '已报名'),  -- 香港运动员报100米青年组
(3, 3, 3, '2025-05-12 10:00:00', '已报名');  -- 澳门运动员报港澳特邀组羽毛球

-- ===================== 裁判与成绩模块 =====================
-- 7. 裁判表（referee）
INSERT INTO referee (name, gender, referee_level, charge_event, phone, bay_cert, multi_language, referee_history)
VALUES 
('黄裁判', '男', '大湾区认证', '龙舟', '13811112222', '有', '中/粤/英', '2024大湾区龙舟赛执裁、2023大湾区运动会执裁'),
('张裁判', '女', '国家级', '100米短跑', '13833334444', '有', '中/英', '2024全国田径锦标赛执裁、2025大湾区运动会执裁'),
('李裁判', '男', '大湾区认证', '羽毛球', '13855556666', '有', '中/粤/葡', '2024澳门羽毛球公开赛执裁、2025大湾区运动会执裁');

-- 8. 裁判组表（referee_group）
INSERT INTO referee_group (group_name, leader_referee_id, event_id)
VALUES 
('龙舟裁判组', 1, 1),
('100米短跑裁判组', 2, 2),
('羽毛球裁判组', 3, 3);

-- 9. 裁判执裁安排表（referee_arrangement）
INSERT INTO referee_arrangement (referee_group_id, referee_id, event_id, arrange_date, position, check_in_status, evaluation)
VALUES 
(1, 1, 1, '2025-06-10 08:00:00', '主裁', '已签到', '执裁规范，无争议'),
(2, 2, 2, '2025-06-11 09:00:00', '主裁', '已签到', '计时准确，判罚公正'),
(3, 3, 3, '2025-06-12 13:00:00', '主裁', '已签到', '规则掌握熟练，多语言沟通顺畅');

-- 10. 成绩表（result）
INSERT INTO result (apply_id, result_value, ranking, round, is_record, wind_speed, score, referee_scores, video_url, appeal_id, score_value, record_cert_status)
VALUES 
(1, '1分50秒', 1, '决赛', '是', 0.5, NULL, '9.8,9.9,9.8', 'https://example.com/video/dragonboat001.mp4', NULL, 10, '已认证'),  -- 龙舟破纪录
(2, '10.2秒', 2, '决赛', '否', 0.2, NULL, NULL, 'https://example.com/video/100m001.mp4', NULL, 8, '未认证'),       -- 100米第二名
(3, '21:18,21:16', 1, '决赛', '否', NULL, 2, '9.7,9.8,9.6', 'https://example.com/video/badminton001.mp4', NULL, 10, '未认证');  -- 羽毛球冠军

-- 11. 奖牌与荣誉表（medal_honor）
INSERT INTO medal_honor (medal_type, athlete_id, team_id, result_id, award_guest, honor_cert_no, public_status, award_time, award_venue)
VALUES 
('金牌', 1, 1, 1, '广东省体育局局长', 'MED-GZ-2025001', '已公示', '2025-06-10 11:00:00', '广州奥体中心'),
('银牌', 2, 2, 2, '香港体育协会主席', 'MED-HK-2025001', '已公示', '2025-06-11 12:00:00', '广州奥体中心'),
('金牌', 3, 3, 3, '澳门体育局局长', 'MED-MO-2025001', '已公示', '2025-06-12 16:00:00', '香港维多利亚公园体育馆');

-- ===================== 后勤保障模块 =====================
-- 12. 供应商表（supplier）
INSERT INTO supplier (supplier_name, service_type, bay_register_address, qualification_url, coop_period, contact_name, contact_phone, performance_score)
VALUES 
('广州餐饮服务有限公司', '餐饮', '广州市天河区天河路100号', 'https://example.com/qual/catering.pdf', '2025-01-01至2025-12-31', '王经理', '13866667777', 4.8),
('香港交通服务有限公司', '交通', '香港九龙尖沙咀弥敦道100号', 'https://example.com/qual/transport.pdf', '2025-01-01至2025-12-31', '陈经理', '13888889999', 4.9),
('澳门器材租赁有限公司', '器材', '澳门半岛新马路100号', 'https://example.com/qual/equipment.pdf', '2025-01-01至2025-12-31', '李经理', '13899990000', 4.7);

-- 13. 后勤保障明细表（logistics_detail）
INSERT INTO logistics_detail (service_type, service_object_type, service_object_id, supplier_id, service_no, cost_amount, service_time, staff_name, satisfaction_score, exception_record)
VALUES 
('餐饮', '运动员', 1, 1, 'LOG-CAT-2025001', 500.00, '2025-06-10 12:00:00', '张厨师', 5, '无'),
('交通', '运动员', 2, 2, 'LOG-TRA-2025001', 1000.00, '2025-06-11 08:00:00', '陈司机', 4, '轻微晚点10分钟'),
('器材', '运动员', 3, 3, 'LOG-EQP-2025001', 2000.00, '2025-06-12 10:00:00', '李技术员', 5, '无');

-- 14. 志愿者表（volunteer）
INSERT INTO volunteer (name, gender, bay_school_company, service_post, service_time_slot, training_status, working_hours, evaluation, phone)
VALUES 
('王同学', '女', '中山大学', '引导', '2025-06-10 08:00-18:00', '已培训', 10.0, '服务热情，指引准确', '13811111111'),
('陈同学', '男', '香港大学', '检录', '2025-06-11 08:00-18:00', '已培训', 10.0, '检录高效，无差错', '13822222222'),
('林同学', '女', '澳门大学', '医疗辅助', '2025-06-12 08:00-18:00', '已培训', 10.0, '应急处理及时', '13833333333');

-- ===================== 赛事运营模块 =====================
-- 15. 赛事日程表（schedule）
INSERT INTO schedule (event_id, venue_id, schedule_date, time_slot, status)
VALUES 
(1, 1, '2025-06-10', '09:00-11:00', '已结束'),
(2, 1, '2025-06-11', '10:00-12:00', '已结束'),
(3, 2, '2025-06-12', '14:00-16:00', '已结束');

-- 16. 赛事运营表（event_operation）
INSERT INTO event_operation (event_id, operation_link, status, staff_id, start_time, end_time, exception_log, bay_approval_status)
VALUES 
(1, '比赛', '已结束', NULL, '2025-06-10 09:00:00', '2025-06-10 11:00:00', '无', '已审批'),
(2, '比赛', '已结束', NULL, '2025-06-11 10:00:00', '2025-06-11 12:00:00', '无', '已审批'),
(3, '比赛', '已结束', NULL, '2025-06-12 14:00:00', '2025-06-12 16:00:00', '无', '已审批');

-- ===================== 申诉与仲裁模块 =====================
-- 17. 申诉表（appeal）
INSERT INTO appeal (athlete_id, event_id, appeal_content, submit_time, status, result, handler_id)
VALUES 
(2, 2, '认为100米短跑成绩计时有误，申请复核（英文：I think the timing of the 100m sprint result is incorrect, apply for review）', '2025-06-11 13:00:00', '已解决', '复核后成绩无误，维持原判', NULL);

-- 18. 仲裁委员会表（arbitration_committee）
INSERT INTO arbitration_committee (committee_name, member_ids, scope, contact_phone, arbitration_process_url)
VALUES 
('大湾区体育仲裁委员会', '1,2,3', '负责大湾区运动会所有申诉仲裁', '13800138004', 'https://example.com/process/arbitration.pdf');

-- 19. 申诉仲裁表（appeal_arbitration）
INSERT INTO appeal_arbitration (appeal_id, committee_id, arbitration_time, arbitration_basis, arbitration_result, public_time, bay_arb条例_reference)
VALUES 
(1, 1, '2025-06-11 15:00:00', '《大湾区体育赛事仲裁规则》第10条', '维持原判，成绩无误', '2025-06-12 00:00:00', '《大湾区体育仲裁条例》2025版第5章第8条');

-- ===================== 商业运营模块 =====================
-- 20. 赞助商表（sponsor）
INSERT INTO sponsor (sponsor_name, sponsor_type, sponsor_value, coop_period, bay_register_address, contact_name, contact_phone)
VALUES 
('广东某体育品牌', '现金', '500万元', '2025-01-01至2025-12-31', '广州市海珠区滨江路100号', '赵经理', '13844445555'),
('香港某集团', '物资', '1000件运动服', '2025-01-01至2025-12-31', '香港中环皇后大道中100号', '钱经理', '13855556666'),
('澳门某酒店', '服务', '100间免费客房', '2025-01-01至2025-12-31', '澳门路氹城金光大道100号', '孙经理', '13866667777');

-- 21. 赞助商权益表（sponsor_rights）
INSERT INTO sponsor_rights (sponsor_id, event_id, rights_type, rights_status, exposure_count, bay_media_channel, finance_id)
VALUES 
(1, 1, '冠名', '已执行', 100000, '广东卫视、大湾区卫视、南方都市报', NULL),
(2, 2, '广告', '已执行', 80000, '香港TVB、香港商报', NULL),
(3, 3, '物料赞助', '已执行', 50000, '澳门日报、澳广视', NULL);

-- 22. 观众票务表（audience_ticket）
INSERT INTO audience_ticket (audience_name, audience_id_card, event_id, seat_no, ticket_price, purchase_channel, refund_status, entry_verification_code, notice_confirm_status, entry_time)
VALUES 
('刘观众', '440101199001011234', 1, 'A1-01', 200.00, '大湾区线上', '未退票', 'VER-GZ-2025001', '已确认', '2025-06-10 08:30:00'),
('陈观众', 'H1234567891', 2, 'B2-02', 300.00, '大湾区线下', '未退票', 'VER-HK-2025001', '已确认', '2025-06-11 09:30:00'),
('李观众', 'M0987654322', 3, 'C3-03', 250.00, '大湾区线上', '未退票', 'VER-MO-2025001', '已确认', '2025-06-12 13:30:00');

-- ===================== 财务与防疫模块 =====================
-- 23. 财务结算表（finance）
INSERT INTO finance (finance_type, amount, related_no, payer_payee, settle_status, bay_tax_record_no)
VALUES 
('报名费', 200.00, 'apply_id_1', '李小华', '已结算', 'TAX-GZ-2025001'),
('赞助费', 5000000.00, 'sponsor_id_1', '广东某体育品牌', '已结算', 'TAX-GZ-2025002'),
('后勤费', 500.00, 'logistics_id_1', '广州餐饮服务有限公司', '已结算', 'TAX-GZ-2025003'),
('奖金', 10000.00, 'medal_honor_id_1', '李小华', '已结算', 'TAX-GZ-2025004');

-- 24. 防疫安全表（epidemic_safety）
INSERT INTO epidemic_safety (person_type, person_id, temperature, safety_training_status, emergency_record)
VALUES 
('运动员', 1, 36.5, '已培训', '无'),
('运动员', 2, 36.6, '已培训', '无'),
('观众', 1, 36.4, '未培训', '无');

-- ===================== 数据统计模块 =====================
-- 25. 数据统计报表表（data_report）
INSERT INTO data_report (stat_dimension, stat_indicator, report_type, stat_data, generate_time, export_status)
VALUES 
('大湾区城市', '参赛人数、奖牌数', '总榜', '{"广州": {"参赛人数": 100, "金牌数": 10}, "香港": {"参赛人数": 80, "金牌数": 8}, "澳门": {"参赛人数": 60, "金牌数": 6}}', '2025-06-15 00:00:00', '已导出'),
('项目', '成绩、破纪录数', '周报', '{"龙舟": {"最好成绩": "1分50秒", "破纪录数": 1}, "100米短跑": {"最好成绩": "10.1秒", "破纪录数": 0}}', '2025-06-14 00:00:00', '未导出'),
('代表队', '积分、获奖数', '日报', '{"广东省广州市代表队": {"积分": 100, "获奖数": 15}, "中国香港代表队": {"积分": 80, "获奖数": 10}}', '2025-06-13 00:00:00', '已导出');