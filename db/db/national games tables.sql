-- 创建数据库（指定UTF8MB4兼容多语言，适配粤/港/澳繁体/英文）
CREATE DATABASE IF NOT EXISTS bay_area_games CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE bay_area_games;

-- 设置时区（适配大湾区东八区）
SET time_zone = '+8:00';

-- 基础信息模块
CREATE TABLE IF NOT EXISTS team (
    team_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '代表队编号',
    team_name VARCHAR(100) NOT NULL COMMENT '代表队名称（如：香港队、深圳队）',
    region VARCHAR(50) NOT NULL COMMENT '所属大湾区城市（广州/深圳/香港/澳门等）',
    city_code CHAR(6) NOT NULL COMMENT '大湾区城市编码（自定义：如01=广州，02=深圳，03=香港）',
    leader_name VARCHAR(50) NOT NULL COMMENT '领队姓名',
    leader_phone VARCHAR(20) NOT NULL COMMENT '领队电话',
    doctor_name VARCHAR(50) COMMENT '队医姓名',
    doctor_phone VARCHAR(20) COMMENT '队医电话',
    logo_url VARCHAR(255) COMMENT '代表队LOGO地址',
    accommodation VARCHAR(255) COMMENT '住宿信息',
    transport VARCHAR(255) COMMENT '交通安排',
    uniform_custom VARCHAR(255) COMMENT '队服定制信息',
    budget DECIMAL(10,2) COMMENT '经费预算',
    insurance_no VARCHAR(50) COMMENT '参赛保险单号',
    physical_report_url VARCHAR(255) COMMENT '体检报告地址', -- 仅保留体检，删除核酸
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (team_id),
    INDEX idx_region (region),
    INDEX idx_city_code (city_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会代表队信息表';

CREATE TABLE IF NOT EXISTS athlete (
    athlete_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '运动员编号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender ENUM('男','女','其他') NOT NULL COMMENT '性别',
    birth_date DATE NOT NULL COMMENT '出生日期',
    id_card VARCHAR(30) COMMENT '身份证号/港澳通行证号/台胞证号',
    bay_area_hukou ENUM('广东','香港','澳门','其他') NOT NULL COMMENT '大湾区户籍',
    height DECIMAL(3,2) COMMENT '身高（米）',
    weight DECIMAL(3,1) COMMENT '体重（公斤）',
    phone VARCHAR(20) COMMENT '联系电话',
    emergency_contact VARCHAR(50) COMMENT '紧急联系人',
    emergency_phone VARCHAR(20) COMMENT '紧急联系人电话',
    health_status VARCHAR(100) COMMENT '健康状况',
    qualification_status ENUM('已审核','未审核','驳回') DEFAULT '未审核' COMMENT '参赛资格状态',
    competition_id VARCHAR(30) UNIQUE COMMENT '参赛证号（唯一）',
    past_records TEXT COMMENT '过往参赛记录',
    doping_test ENUM('合格','不合格','待检测') DEFAULT '待检测' COMMENT '兴奋剂检测结果',
    clothing_size VARCHAR(20) COMMENT '服装尺码',
    insurance_info VARCHAR(255) COMMENT '保险信息',
    team_id INT UNSIGNED NOT NULL COMMENT '所属代表队编号',
    join_time DATETIME COMMENT '入队时间',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (athlete_id),
    INDEX idx_team_id (team_id),
    INDEX idx_bay_area_hukou (bay_area_hukou),
    INDEX idx_qualification_status (qualification_status),
    FOREIGN KEY (team_id) REFERENCES team(team_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会运动员信息表';

-- 赛事项目模块
CREATE TABLE IF NOT EXISTS venue (
    venue_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '场地编号',
    venue_name VARCHAR(100) NOT NULL COMMENT '场地名称',
    capacity INT UNSIGNED COMMENT '容纳人数',
    address VARCHAR(255) NOT NULL COMMENT '场地地址',
    facility_status ENUM('正常','维修中','停用') DEFAULT '正常' COMMENT '设施状态',
    manager_name VARCHAR(50) COMMENT '场地负责人',
    manager_phone VARCHAR(20) COMMENT '负责人电话',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (venue_id),
    INDEX idx_venue_name (venue_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会比赛场地表';

CREATE TABLE IF NOT EXISTS event (
    event_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '项目编号',
    event_name VARCHAR(100) NOT NULL COMMENT '项目名称（多语言：如100米短跑/100m Sprint/100米短跑）',
    event_type VARCHAR(50) NOT NULL COMMENT '项目类型（田径/游泳/球类/大湾区传统项目等）',
    gender_limit ENUM('男','女','混合') NOT NULL COMMENT '性别限制',
    player_limit INT UNSIGNED COMMENT '参赛人数限制',
    event_time DATETIME COMMENT '比赛时间',
    venue_id INT UNSIGNED NOT NULL COMMENT '比赛场地编号',
    rule_doc_url VARCHAR(255) COMMENT '项目规则文档地址',
    apply_deadline DATETIME COMMENT '报名截止时间',
    referee_group_id INT UNSIGNED COMMENT '裁判组编号',
    bay_feature ENUM('是','否') DEFAULT '否' COMMENT '是否大湾区特色项目（醒狮/龙舟等）',
    score_rule TEXT COMMENT '项目积分规则',
    live_url VARCHAR(255) COMMENT '直播流地址',
    equipment_list TEXT COMMENT '器材清单',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (event_id),
    INDEX idx_event_type (event_type),
    INDEX idx_venue_id (venue_id),
    INDEX idx_bay_feature (bay_feature),
    FOREIGN KEY (venue_id) REFERENCES venue(venue_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会比赛项目表';

CREATE TABLE IF NOT EXISTS `group` (
    group_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '分组编号',
    group_name VARCHAR(100) NOT NULL COMMENT '分组名称（如：甲组青年/乙组成年/港澳特邀组）',
    age_range VARCHAR(50) COMMENT '年龄范围（如：18-25岁）',
    rule TEXT COMMENT '分组规则',
    disability_integration ENUM('是','否') DEFAULT '否' COMMENT '残健融合分组标记',
    event_id INT UNSIGNED NOT NULL COMMENT '所属项目编号',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (group_id),
    INDEX idx_event_id (event_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会赛事分组表';

CREATE TABLE IF NOT EXISTS athlete_event (
    apply_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '报名编号',
    athlete_id INT UNSIGNED NOT NULL COMMENT '运动员编号',
    event_id INT UNSIGNED NOT NULL COMMENT '项目编号',
    group_id INT UNSIGNED NOT NULL COMMENT '分组编号',
    apply_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
    apply_status ENUM('已报名','已取消','审核中') DEFAULT '审核中' COMMENT '报名状态',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (apply_id),
    UNIQUE KEY uk_athlete_event (athlete_id, event_id, group_id), -- 同一运动员不可重复报名同一项目同一分组
    INDEX idx_athlete_id (athlete_id),
    INDEX idx_event_id (event_id),
    FOREIGN KEY (athlete_id) REFERENCES athlete(athlete_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (group_id) REFERENCES `group`(group_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会运动员项目报名表';

-- 裁判与成绩模块
CREATE TABLE IF NOT EXISTS referee (
    referee_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '裁判编号',
    name VARCHAR(50) NOT NULL COMMENT '裁判姓名',
    gender ENUM('男','女','其他') NOT NULL COMMENT '性别',
    referee_level ENUM('国家级','省级','大湾区认证') NOT NULL COMMENT '裁判等级',
    charge_event VARCHAR(100) COMMENT '负责项目',
    phone VARCHAR(20) COMMENT '联系电话',
    bay_cert ENUM('有','无') DEFAULT '无' COMMENT '大湾区裁判资质认证',
    multi_language VARCHAR(50) COMMENT '多语言能力（中/英/粤）',
    referee_history TEXT COMMENT '执裁历史（大湾区赛事）',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (referee_id),
    INDEX idx_referee_level (referee_level),
    INDEX idx_bay_cert (bay_cert)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会裁判信息表';

CREATE TABLE IF NOT EXISTS referee_group (
    referee_group_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '裁判组编号',
    group_name VARCHAR(100) NOT NULL COMMENT '裁判组名称（如：田径预赛组/游泳决赛组）',
    leader_referee_id INT UNSIGNED COMMENT '组长裁判编号',
    event_id INT UNSIGNED NOT NULL COMMENT '负责项目编号',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (referee_group_id),
    INDEX idx_event_id (event_id),
    INDEX idx_leader_referee_id (leader_referee_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (leader_referee_id) REFERENCES referee(referee_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会裁判组表';

CREATE TABLE IF NOT EXISTS referee_arrangement (
    arrange_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '执裁安排编号',
    referee_group_id INT UNSIGNED NOT NULL COMMENT '裁判组编号',
    referee_id INT UNSIGNED NOT NULL COMMENT '裁判编号',
    event_id INT UNSIGNED NOT NULL COMMENT '执裁项目编号',
    arrange_date DATETIME NOT NULL COMMENT '执裁日期',
    position VARCHAR(50) COMMENT '执裁岗位（主裁/边裁/计时员）',
    check_in_status ENUM('已签到','未签到') DEFAULT '未签到' COMMENT '签到状态',
    evaluation VARCHAR(255) COMMENT '执裁评价',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (arrange_id),
    INDEX idx_referee_id (referee_id),
    INDEX idx_event_id (event_id),
    FOREIGN KEY (referee_group_id) REFERENCES referee_group(referee_group_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (referee_id) REFERENCES referee(referee_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会裁判执裁安排表';

CREATE TABLE IF NOT EXISTS result (
    result_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '成绩编号',
    apply_id INT UNSIGNED NOT NULL COMMENT '报名编号',
    result_value VARCHAR(50) NOT NULL COMMENT '成绩数值（如10.5秒/5000米/90分）',
    ranking INT UNSIGNED COMMENT '成绩排名',
    round ENUM('预赛','复赛','决赛') COMMENT '比赛轮次',
    is_record ENUM('是','否') DEFAULT '否' COMMENT '是否破纪录',
    wind_speed DECIMAL(3,2) COMMENT '风速（田径项目）',
    score INT COMMENT '得分（球类项目）',
    referee_scores TEXT COMMENT '裁判打分（如体操/跳水）',
    video_url VARCHAR(255) COMMENT '视频回放地址',
    appeal_id INT UNSIGNED COMMENT '申诉关联ID',
    score_value INT COMMENT '积分值',
    record_cert_status ENUM('已认证','未认证') DEFAULT '未认证' COMMENT '破纪录认证状态',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (result_id),
    UNIQUE KEY uk_apply_id (apply_id), -- 一条报名对应一条成绩
    INDEX idx_ranking (ranking),
    INDEX idx_is_record (is_record),
    FOREIGN KEY (apply_id) REFERENCES athlete_event(apply_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会比赛成绩表';

CREATE TABLE IF NOT EXISTS medal_honor (
    medal_honor_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '奖牌荣誉编号',
    medal_type ENUM('金牌','银牌','铜牌','集体奖','道德风尚奖') NOT NULL COMMENT '奖牌/荣誉类型',
    athlete_id INT UNSIGNED COMMENT '获奖运动员编号（个人奖）',
    team_id INT UNSIGNED COMMENT '获奖团队编号（集体奖）',
    result_id INT UNSIGNED NOT NULL COMMENT '关联成绩编号',
    award_guest VARCHAR(50) COMMENT '颁奖嘉宾',
    honor_cert_no VARCHAR(50) COMMENT '荣誉证书编号',
    public_status ENUM('已公示','未公示') DEFAULT '未公示' COMMENT '公示状态',
    award_time DATETIME COMMENT '颁发时间',
    award_venue VARCHAR(100) COMMENT '颁奖地点',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (medal_honor_id),
    INDEX idx_athlete_id (athlete_id),
    INDEX idx_team_id (team_id),
    INDEX idx_result_id (result_id),
    FOREIGN KEY (athlete_id) REFERENCES athlete(athlete_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (team_id) REFERENCES team(team_id) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (result_id) REFERENCES result(result_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会奖牌与荣誉表';

-- 后勤保障模块
CREATE TABLE IF NOT EXISTS supplier (
    supplier_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '供应商编号',
    supplier_name VARCHAR(100) NOT NULL COMMENT '供应商名称',
    service_type VARCHAR(50) NOT NULL COMMENT '服务类型（餐饮/器材/交通/住宿）',
    bay_register_address VARCHAR(255) COMMENT '大湾区注册地址',
    qualification_url VARCHAR(255) COMMENT '资质证书地址',
    coop_period VARCHAR(50) COMMENT '合作期限',
    contact_name VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系人电话',
    performance_score DECIMAL(2,1) COMMENT '履约评分',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (supplier_id),
    INDEX idx_service_type (service_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会供应商表';

CREATE TABLE IF NOT EXISTS logistics_detail (
    logistics_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '保障编号',
    service_type ENUM('餐饮','住宿','医疗','交通','器材') NOT NULL COMMENT '保障类型',
    service_object_type ENUM('运动员','裁判','工作人员') NOT NULL COMMENT '服务对象类型',
    service_object_id INT UNSIGNED NOT NULL COMMENT '服务对象ID（运动员/裁判/工作人员编号）',
    supplier_id INT UNSIGNED COMMENT '供应商编号',
    service_no VARCHAR(50) COMMENT '服务单号',
    cost_amount DECIMAL(10,2) COMMENT '费用金额',
    service_time DATETIME COMMENT '服务时间',
    staff_name VARCHAR(50) COMMENT '服务人员',
    satisfaction_score TINYINT UNSIGNED COMMENT '满意度评分（1-5分）',
    exception_record TEXT COMMENT '异常记录',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (logistics_id),
    INDEX idx_service_object (service_object_type, service_object_id),
    INDEX idx_supplier_id (supplier_id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(supplier_id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会后勤保障明细表';

CREATE TABLE IF NOT EXISTS volunteer (
    volunteer_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '志愿者编号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    gender ENUM('男','女','其他') NOT NULL COMMENT '性别',
    bay_school_company VARCHAR(100) COMMENT '大湾区院校/单位',
    service_post VARCHAR(50) COMMENT '服务岗位（引导/检录/医疗辅助）',
    service_time_slot VARCHAR(100) COMMENT '服务时段',
    training_status ENUM('已培训','未培训') DEFAULT '未培训' COMMENT '培训状态',
    working_hours DECIMAL(4,1) DEFAULT 0 COMMENT '服务工时',
    evaluation VARCHAR(255) COMMENT '服务评价',
    phone VARCHAR(20) COMMENT '联系电话',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (volunteer_id),
    INDEX idx_service_post (service_post),
    INDEX idx_training_status (training_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会志愿者表';

-- 赛事运营模块
CREATE TABLE IF NOT EXISTS schedule (
    schedule_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '日程编号',
    event_id INT UNSIGNED NOT NULL COMMENT '项目编号',
    venue_id INT UNSIGNED NOT NULL COMMENT '场地编号',
    schedule_date DATE NOT NULL COMMENT '日程日期',
    time_slot VARCHAR(50) NOT NULL COMMENT '时间段（如：09:00-10:30）',
    status ENUM('未开始','进行中','已结束') DEFAULT '未开始' COMMENT '日程状态',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (schedule_id),
    INDEX idx_event_id (event_id),
    INDEX idx_venue_id (venue_id),
    INDEX idx_schedule_date (schedule_date),
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (venue_id) REFERENCES venue(venue_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会赛事日程表';

CREATE TABLE IF NOT EXISTS event_operation (
    operation_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '运营环节编号',
    event_id INT UNSIGNED NOT NULL COMMENT '项目编号',
    operation_link ENUM('报名','检录','比赛','颁奖','申诉') NOT NULL COMMENT '运营环节',
    status ENUM('未开始','进行中','已结束') DEFAULT '未开始' COMMENT '环节状态',
    staff_id INT UNSIGNED COMMENT '负责人编号',
    start_time DATETIME COMMENT '开始时间',
    end_time DATETIME COMMENT '结束时间',
    exception_log TEXT COMMENT '异常日志',
    bay_approval_status ENUM('已审批','未审批') DEFAULT '未审批' COMMENT '大湾区专项审批状态',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (operation_id),
    INDEX idx_event_id (event_id),
    INDEX idx_operation_link (operation_link),
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会赛事运营表';

-- 申诉与仲裁模块
CREATE TABLE IF NOT EXISTS appeal (
    appeal_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '申诉编号',
    athlete_id INT UNSIGNED NOT NULL COMMENT '申诉运动员编号',
    event_id INT UNSIGNED NOT NULL COMMENT '申诉项目编号',
    appeal_content TEXT NOT NULL COMMENT '申诉内容（多语言）',
    submit_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
    status ENUM('待处理','已受理','已驳回','已解决') DEFAULT '待处理' COMMENT '处理状态',
    result TEXT COMMENT '处理结果',
    handler_id INT UNSIGNED COMMENT '处理人编号',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (appeal_id),
    INDEX idx_athlete_id (athlete_id),
    INDEX idx_event_id (event_id),
    INDEX idx_status (status),
    FOREIGN KEY (athlete_id) REFERENCES athlete(athlete_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会申诉表';

CREATE TABLE IF NOT EXISTS arbitration_committee (
    committee_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '委员会编号',
    committee_name VARCHAR(100) NOT NULL COMMENT '委员会名称',
    member_ids TEXT COMMENT '成员ID（大湾区专家/律师/裁判，逗号分隔）',
    scope VARCHAR(255) COMMENT '职责范围',
    contact_phone VARCHAR(20) COMMENT '联系方式',
    arbitration_process_url VARCHAR(255) COMMENT '仲裁流程文档地址',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (committee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会仲裁委员会表';

CREATE TABLE IF NOT EXISTS appeal_arbitration (
    arbitration_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '仲裁编号',
    appeal_id INT UNSIGNED NOT NULL COMMENT '申诉编号',
    committee_id INT UNSIGNED NOT NULL COMMENT '仲裁委员会编号',
    arbitration_time DATETIME COMMENT '仲裁时间',
    arbitration_basis TEXT COMMENT '仲裁依据',
    arbitration_result TEXT NOT NULL COMMENT '仲裁结果',
    public_time DATETIME COMMENT '公示时间',
    bay_arb条例_reference VARCHAR(255) COMMENT '大湾区体育仲裁条例引用',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (arbitration_id),
    UNIQUE KEY uk_appeal_id (appeal_id),
    INDEX idx_committee_id (committee_id),
    FOREIGN KEY (appeal_id) REFERENCES appeal(appeal_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (committee_id) REFERENCES arbitration_committee(committee_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会申诉仲裁表';

-- 商业运营模块
CREATE TABLE IF NOT EXISTS sponsor (
    sponsor_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '赞助商编号',
    sponsor_name VARCHAR(100) NOT NULL COMMENT '赞助商名称',
    sponsor_type ENUM('现金','物资','服务') NOT NULL COMMENT '赞助类型',
    sponsor_value VARCHAR(100) NOT NULL COMMENT '赞助金额/物资（如：100万元/1000件运动服）',
    coop_period VARCHAR(50) COMMENT '合作期限',
    bay_register_address VARCHAR(255) COMMENT '大湾区注册地址',
    contact_name VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系人电话',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (sponsor_id),
    INDEX idx_sponsor_type (sponsor_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会赞助商表';

CREATE TABLE IF NOT EXISTS sponsor_rights (
    rights_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '权益编号',
    sponsor_id INT UNSIGNED NOT NULL COMMENT '赞助商编号',
    event_id INT UNSIGNED NOT NULL COMMENT '项目编号',
    rights_type ENUM('冠名','广告','颁奖','物料赞助') NOT NULL COMMENT '权益类型',
    rights_status ENUM('已执行','未执行','部分执行') DEFAULT '未执行' COMMENT '权益执行状态',
    exposure_count INT UNSIGNED DEFAULT 0 COMMENT '曝光次数',
    bay_media_channel VARCHAR(255) COMMENT '大湾区媒体投放渠道',
    finance_id INT UNSIGNED COMMENT '关联财务结算编号',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (rights_id),
    INDEX idx_sponsor_id (sponsor_id),
    INDEX idx_event_id (event_id),
    FOREIGN KEY (sponsor_id) REFERENCES sponsor(sponsor_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会赞助商权益表';

CREATE TABLE IF NOT EXISTS audience_ticket (
    ticket_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '票务编号',
    audience_name VARCHAR(50) NOT NULL COMMENT '观众姓名',
    audience_id_card VARCHAR(30) COMMENT '观众身份证号/港澳通行证号',
    event_id INT UNSIGNED NOT NULL COMMENT '观赛项目编号',
    seat_no VARCHAR(20) COMMENT '座位号',
    ticket_price DECIMAL(8,2) COMMENT '票价',
    purchase_channel ENUM('大湾区线上','大湾区线下','其他') COMMENT '购票渠道',
    refund_status ENUM('未退票','已退票') DEFAULT '未退票' COMMENT '退票状态',
    entry_verification_code VARCHAR(50) COMMENT '入场核验码',
    notice_confirm_status ENUM('已确认','未确认') DEFAULT '未确认' COMMENT '观赛须知确认状态',
    entry_time DATETIME COMMENT '入场时间',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (ticket_id),
    INDEX idx_event_id (event_id),
    INDEX idx_audience_id_card (audience_id_card),
    FOREIGN KEY (event_id) REFERENCES event(event_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会观众票务表';

-- 财务与防疫模块
CREATE TABLE IF NOT EXISTS finance (
    finance_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '财务编号',
    finance_type ENUM('报名费','赞助费','后勤费','奖金','其他') NOT NULL COMMENT '收支类型',
    amount DECIMAL(10,2) NOT NULL COMMENT '金额',
    related_no VARCHAR(50) COMMENT '关联单号（报名单号/赞助单号/后勤单号）',
    payer_payee VARCHAR(100) COMMENT '付款/收款方',
    settle_status ENUM('已结算','未结算') DEFAULT '未结算' COMMENT '结算状态',
    bay_tax_record_no VARCHAR(50) COMMENT '大湾区税务备案号',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (finance_id),
    INDEX idx_finance_type (finance_type),
    INDEX idx_related_no (related_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会财务结算表';

CREATE TABLE IF NOT EXISTS epidemic_safety (
    es_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '防疫安全编号',
    person_type ENUM('运动员','观众','工作人员') NOT NULL COMMENT '人员类型',
    person_id INT UNSIGNED NOT NULL COMMENT '人员ID（运动员/观众/工作人员编号）',
    temperature DECIMAL(3,1) COMMENT '体温记录',
    safety_training_status ENUM('已培训','未培训') DEFAULT '未培训' COMMENT '安全培训状态',
    emergency_record TEXT COMMENT '应急事件记录',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (es_id),
    INDEX idx_person (person_type, person_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会防疫安全表';

-- 数据统计模块
CREATE TABLE IF NOT EXISTS data_report (
    report_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '报表编号',
    stat_dimension VARCHAR(50) NOT NULL COMMENT '统计维度（大湾区城市/项目/代表队/运动员）',
    stat_indicator VARCHAR(100) NOT NULL COMMENT '统计指标（参赛人数/奖牌数/成绩/积分）',
    report_type ENUM('日报','周报','总榜','专项') NOT NULL COMMENT '报表类型',
    stat_data TEXT NOT NULL COMMENT '统计数据（JSON格式）',
    generate_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '生成时间',
    export_status ENUM('已导出','未导出') DEFAULT '未导出' COMMENT '导出状态',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (report_id),
    INDEX idx_stat_dimension (stat_dimension),
    INDEX idx_report_type (report_type),
    INDEX idx_generate_time (generate_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='大湾区运动会数据统计报表表';