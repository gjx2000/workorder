#! /usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from workapp.models import User
from workapp import models

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField()
    # password = serializers.CharField()
    mobile = serializers.CharField()
    email = serializers.CharField()
    weixinid = serializers.CharField()
    token = serializers.CharField(read_only=True)
    ur = serializers.SerializerMethodField()
    depts = serializers.SerializerMethodField()
    class Meta:
        model=User
    def create(self, data):
        user = User.objects.create(**data)
        user.set_password(data.get('password'))
        user.save()
        # 补充生成记录登录状态的token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user
    def get_ur(self, row):
        gp = row.ur.all().values('zh_name')
        return gp

    def get_depts(self, row):
        depts = row.department_set.all().values('name')  # 表名_set 反向多对多
        return depts

class RoleSerializer(serializers.Serializer):
    name = serializers.CharField()
    zh_name = serializers.CharField()
    class Meta:
        model=models.Role

class FlowconfSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    callback = serializers.CharField()
    creator = serializers.CharField(source='creator.username')
    class Meta:
        model=models.FlowConf
class DepartmentSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    class Meta:
        model=models.Department

class NewFlowUserRoleActionConfSerializer(serializers.Serializer):
    id = serializers.CharField()
    sequence = serializers.IntegerField()
    approve_type_id = serializers.CharField()
    flowconf = serializers.CharField(source='flowconf.name')
    approvetorole = serializers.CharField()
    is_auto = serializers.CharField()
    class Meta:
        models = models.NewFlowUserRoleActionConf




