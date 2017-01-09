# -*- coding:utf-8 -*-


from rest_framework import serializers
from module_payment.models import Payment, PaymentRecord, PaymentRefund
import uuid

def validate_uuid(value):
    if value == "" or value == None:
        return True
    try:
        uuid.UUID(value)
    except ValueError:
        raise serializers.ValidationError(u"uuid非法")
    return True

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentCreateSerializer(serializers.ModelSerializer):
    real_price = serializers.SerializerMethodField()
    payment_no = serializers.SerializerMethodField()
    is_valid = serializers.SerializerMethodField()
    paid_status = serializers.SerializerMethodField()
    paid_method = serializers.SerializerMethodField()

    user_uuid = serializers.CharField(required=False, max_length=50)
    # payment_account_uuid = serializers.CharField(required=False, validators=[validate_uuid])
    # coupon_uuid = serializers.CharField(required=False, validators=[validate_uuid])
    def get_real_price(self, obj):
        return obj.real_price

    def get_payment_no(self, obj):
        return obj.payment_no

    def get_is_valid(self, obj):
        return True

    def get_paid_status(self, obj):
        return obj.paid_status

    def get_paid_method(self, obj):
        return obj.paid_method
        
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentRefundSerializer(serializers.ModelSerializer):
    payment_uuid = serializers.SerializerMethodField()

    def get_payment_uuid(self, obj):
        return unicode(obj.payment_uuid)
    class Meta:
        model = PaymentRefund
        fields = '__all__'


class PaymentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRecord
        fields = '__all__'

