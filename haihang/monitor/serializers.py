# -*- coding:utf-8 -*-
from rest_framework import serializers
from models import AlertRecord


class AlertRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertRecord
        fields = "__all__"


