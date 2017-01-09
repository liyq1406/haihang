# -*- coding:utf-8 -*-

from rest_framework import serializers
from models import Reconciliation


class ReconciliationDealSerializer(serializers.ModelSerializer):
    deal_result = serializers.SerializerMethodField()
    deal_status = serializers.SerializerMethodField()
    third_record = serializers.SerializerMethodField()
    error_type = serializers.SerializerMethodField()

    def get_deal_result(self, obj):
        return obj.deal_result

    def get_deal_status(self, obj):
        return obj.deal_status

    def get_third_record(self, obj):
        return obj.third_record

    def get_error_type(self, obj):
        return obj.error_type

    class Meta:
        model = Reconciliation
        fields = '__all__'


class ReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reconciliation
        exclude = ('payment_record', 'third_record',)


class ReconciliationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reconciliation
        fields = '__all__'