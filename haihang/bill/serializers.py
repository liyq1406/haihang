# -*- coding:utf-8 -*-
# !/usr/bin/python

from rest_framework import serializers
from bill.models import Bill


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        # fields = '__all__'
        fields = ('user_uuid', 'bill_uuid', 'host_uuid', 'total_fee', 'pay_status',
                  'bill_createtime', 'bill_account_time','name')


class BillSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Bill
        # fields = '__all__'
        fields = ('user_uuid',)


class BillUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=20)

    def get_name(self, obj):
        return obj['name']

    def create(self, validated_data):
        return validated_data

    class Meta:
        model = Bill
        fields = ('name', 'user_uuid', 'user_uuid', 'container_uuid')
