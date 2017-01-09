# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from Payment.validates import non_negative
from django.db import models
import uuid

# 支付方式
PAID_METHOD = (
    ('alipay', 'alipay'),
    ('paypal', 'paypal'),
    ('coupon', 'coupon'),
)

# 订单状态
PAID_STATUS = (
    ('created', 'created'),
    ('waiting', 'waiting'),
    ('success', 'success'),
    ('failed', 'failed'),
    ('refunded', 'refunded'),
    ('canceled', 'canceled'),
)

# 退款状态
REFUND_STATUS = (
    ('waiting', 'waiting'),
    ('success', 'success'),
    ('refuse', 'refuse'),
)


# Create your models here.
class Payment(models.Model):
    """
    支付单模型
    """
    payment_uuid = models.UUIDField(primary_key=True,default=uuid.uuid1, editable=False)
    # user_uuid 与 payment_account_uuid选填一个
    user_uuid = models.CharField(blank=True, max_length=36)
    payment_account_uuid = models.CharField(blank=True, max_length=36)
    payment_no = models.CharField(max_length=50, blank=True)
    payment_price = models.IntegerField(validators=[non_negative])
    paid_method = models.CharField(choices=PAID_METHOD, max_length=10, default='none')
    real_price = models.FloatField()
    # 交易号, alipay, paypal退货依据
    sale_id = models.CharField(blank=True, max_length=64)
    is_valid = models.BooleanField(default=True)
    # 优惠码使用时, uuid和code选填一个
    coupon_uuid = models.CharField(blank=True, max_length=36)
    coupon_code = models.CharField(blank=True, max_length=10)
    paid_status = models.CharField(choices=PAID_STATUS, max_length=10, default='created')
    create_time = models.DateTimeField(auto_now_add=True)

    def _unicode__(self):
        return unicode(self.payment_uuid)


class PaymentRecord(models.Model):
    """
    支付单处理记录模型
    """
    payment_record_uuid = models.UUIDField(primary_key=True,default=uuid.uuid1, editable=False)
    payment_uuid = models.ForeignKey('Payment', related_name='payment_rc')
    paid_method = models.CharField(choices=PAID_METHOD, max_length=10, default='none')
    pay_response_data = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.payment_record_uuid)

class PaymentRefund(models.Model):
    """
    支付单退款模型
    """
    payment_refund_uuid = models.UUIDField(primary_key=True,default=uuid.uuid1, editable=False)
    payment_uuid = models.ForeignKey('Payment', related_name='payment_rf')
    refund_reason = models.CharField(max_length=300)
    refund_status = models.CharField(choices=REFUND_STATUS, max_length=10, default='waiting')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.payment_refund_uuid)
        