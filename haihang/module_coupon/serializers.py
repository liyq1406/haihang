# -*- coding:utf-8 -*-

from rest_framework import serializers
from module_coupon.models import Coupon, CouponUser, CouponUsage
from Payment.validates import in_range

class CouponCreateSerializer(serializers.ModelSerializer):
    create_count = serializers.IntegerField(validators=[in_range])
    coupon_codes = serializers.SerializerMethodField()
    coupon_path = serializers.SerializerMethodField()
    def get_coupon_codes(self, obj):
        return obj['coupon_codes']

    def get_coupon_path(self, obj):
        return obj['coupon_path']

    def create(self, validated_data):
        # 该接口仅用于serializers数据,不做保存操作
        return validated_data

    class Meta:
        model = Coupon
        fields = ('create_count', 'coupon_type', 'coupon_using_count', 'coupon_codes', 'coupon_path',
                  'coupon_using_user', 'coupon_value', 'valid_datetime_start', 'valid_datetime_end')


class CouponSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class CouponUsageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CouponUsage
        fields = '__all__'

class CouponUserSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CouponUser
        fields = '__all__'


class CouponUseSerialzer(serializers.ModelSerializer):
    coupon_uuid = serializers.SerializerMethodField()
    payment_account_uuid = serializers.SerializerMethodField()
    coupon_code = serializers.SerializerMethodField()
    usage_source_uuid = serializers.SerializerMethodField()
    use_time = serializers.SerializerMethodField()

    def get_coupon_uuid(self, obj):
        return unicode(obj['coupon_uuid'])

    def get_payment_account_uuid(self, obj):
        return obj['payment_account_uuid']

    def get_usage_source_uuid(self, obj):
        return obj['usage_source_uuid']
    
    def get_coupon_code(self, obj):
        return obj['coupon_code']
    
    def get_use_time(self, obj):
        return obj['use_time']
        
    def create(self, validated_data):
        return validated_data

    class Meta:
        model = CouponUsage
        fields = ('coupon_usage_uuid', 'user_uuid', 'payment_account_uuid', 'coupon_uuid',
                  'use_time', 'usage_source_type', 'usage_source_uuid', 'coupon_code')
