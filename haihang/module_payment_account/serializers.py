# -*- coding:utf-8 -*-

from rest_framework import serializers
from module_payment_account.models import PaymentAccount, AccountRecord
from django.utils import timezone
from bill.util import get_bill_byuserid


class PaymentAccountListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAccount
        fields = '__all__'


class PaymentAccountUpdateSerializer(serializers.ModelSerializer):
    account_record_uuid = serializers.SerializerMethodField()
    modify_balance = serializers.FloatField()
    modify_source_type = serializers.ChoiceField(choices=['payment', 'bill', 'coupon_usage'], allow_blank=False)
    modify_source_uuid = serializers.CharField(allow_blank=True, max_length=36)
    update_time = serializers.SerializerMethodField()

    def get_update_time(self, obj):
        return timezone.now()

    def get_account_record_uuid(self, obj):
        return obj.account_record_uuid

    class Meta:
        model = PaymentAccount
        fields = ('payment_account_uuid', 'account_record_uuid', 'modify_balance', 
                  'is_valid', 'modify_source_type', 'modify_source_uuid', 'update_time')


class PaymentAccountRetrieveSerializer(serializers.ModelSerializer):
    view_balance = serializers.SerializerMethodField()

    def get_view_balance(self, obj):
        bills = get_bill_byuserid(obj.user_uuid)
        if not bills:
            return obj.balance
        total = 0
        for bill in bills:
            total += bill.total_fee
        return obj.balance - total

    class Meta:
        model = PaymentAccount
        fields = ('payment_account_uuid', 'user_uuid', 'view_balance',
                  'balance', 'is_valid', 'credit', 'create_time')


class AccountRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountRecord
        fields = '__all__'

