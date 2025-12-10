import os
from rest_framework import serializers

from .models import Athlete, Team


class TeamSerializer(serializers.ModelSerializer):
    athletes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = "__all__"
    
    def get_athletes_count(self, obj):
        return obj.athletes.count()
    
    def create(self, validated_data):
        # 确保team_code有默认值
        if 'team_code' not in validated_data or not validated_data['team_code']:
            region = validated_data.get('region', '')
            code_map = {'广州': 'GZ', '深圳': 'SZ', '香港': 'HK', '澳门': 'MO'}
            validated_data['team_code'] = code_map.get(region, 'OT')
        # 确保sport_type有默认值
        if 'sport_type' not in validated_data or not validated_data['sport_type']:
            validated_data['sport_type'] = '综合'
        # 确保is_active有默认值
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
        return super().create(validated_data)


class AthleteSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.team_name', read_only=True)
    team_id = serializers.IntegerField(source='team.id', read_only=True)
    
    class Meta:
        model = Athlete
        fields = "__all__"
    
    def create(self, validated_data):
        # 确保id_card有默认值（空字符串），因为数据库表可能要求NOT NULL
        if 'id_card' not in validated_data or validated_data['id_card'] is None:
            validated_data['id_card'] = ''
        
        # 确保phone有默认值
        if 'phone' not in validated_data or validated_data['phone'] is None:
            validated_data['phone'] = ''
        
        # 计算age（数据库表需要但模型中没有）
        from datetime import date, datetime
        birth_date = validated_data.get('birth_date')
        age = 25  # 默认年龄
        if birth_date:
            if isinstance(birth_date, str):
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            if isinstance(birth_date, date):
                today = date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # 使用raw SQL插入，包含所有数据库表需要的字段
        from django.db import connection
        from django.utils import timezone
        import sqlite3
        
        # 获取数据库路径
        db_path = connection.settings_dict['NAME']
        if not os.path.isabs(db_path):
            from django.conf import settings
            db_path = str(settings.BASE_DIR / db_path)
        
        # 准备所有字段的值
        now = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 获取team_id
        team_id = validated_data['team']
        if hasattr(team_id, 'id'):
            team_id = team_id.id
        
        # 格式化birth_date
        birth_date_str = validated_data['birth_date']
        if isinstance(birth_date_str, date):
            birth_date_str = birth_date_str.strftime('%Y-%m-%d')
        elif isinstance(birth_date_str, str):
            pass  # 已经是字符串格式
        else:
            birth_date_str = str(birth_date_str)
        
        # 使用直接SQLite连接插入
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # 检查表结构
            cursor.execute('PRAGMA table_info(basic_info_athlete)')
            table_cols = [col[1] for col in cursor.fetchall()]
            
            # 根据表结构构建参数
            base_params = [
                validated_data['name'],
                validated_data.get('id_card', ''),
                validated_data['gender'],
            ]
            
            # 如果有age字段，计算年龄
            if 'age' in table_cols:
                birth_date = validated_data.get('birth_date')
                age = 25  # 默认年龄
                if birth_date:
                    if isinstance(birth_date, str):
                        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
                    if isinstance(birth_date, date):
                        today = date.today()
                        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                base_params.append(age)
            
            # 如果有position字段
            if 'position' in table_cols:
                base_params.append('运动员')  # position默认值
            
            # 继续添加其他字段（只添加存在的字段）
            base_params.extend([
                validated_data.get('phone', ''),
                now,  # create_time
                now,  # update_time
            ])
            
            # 如果有is_active字段
            if 'is_active' in table_cols:
                base_params.append(1)  # is_active
            
            base_params.extend([
                team_id,  # team_id
                birth_date_str,  # birth_date
                validated_data['bay_area_hukou'],
                validated_data.get('doping_test', '待检测'),
                validated_data.get('qualification_status', '未审核'),
            ])
            
            params = base_params
            
            # 构建INSERT语句的字段列表
            field_names = ['name', 'id_card', 'gender']
            if 'age' in table_cols:
                field_names.append('age')
            if 'position' in table_cols:
                field_names.append('position')
            field_names.extend(['phone', 'create_time', 'update_time'])
            if 'is_active' in table_cols:
                field_names.append('is_active')
            field_names.extend([
                'team_id',
                'birth_date', 'bay_area_hukou', 'doping_test', 'qualification_status'
            ])
            
            # 构建INSERT语句
            placeholders = ','.join(['?' for _ in field_names])
            field_list = ','.join(field_names)
            cursor.execute(f'''
                INSERT INTO basic_info_athlete ({field_list})
                VALUES ({placeholders})
            ''', params)
            
            athlete_id = cursor.lastrowid
            conn.commit()
        finally:
            conn.close()
        
        # 返回实例
        from .models import Athlete
        instance = Athlete.objects.get(pk=athlete_id)
        
        # 更新可选字段
        optional_fields = ['height', 'weight', 'emergency_contact', 'emergency_phone', 
                          'health_status', 'clothing_size', 'insurance_info', 'competition_id', 'past_records']
        update_data = {}
        for field in optional_fields:
            if field in validated_data and validated_data[field] is not None:
                update_data[field] = validated_data[field]
        
        if update_data:
            for key, value in update_data.items():
                setattr(instance, key, value)
            instance.save(update_fields=list(update_data.keys()))
        
        return instance
    
    def update(self, instance, validated_data):
        # 确保id_card有默认值
        if 'id_card' in validated_data and validated_data['id_card'] is None:
            validated_data['id_card'] = ''
        return super().update(instance, validated_data)

