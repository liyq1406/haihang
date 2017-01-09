# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from Payment.initConf import MODULE_COUPON
from Payment.validates import positive
from django.db import models
import uuid

# 优惠码类型:支付单(充值)/账单(扣费)/优惠码使用(充值)
COUPON_TYPE = (
    ('discount', 'discount'),
    ('reduce', 'reduce'),
    ('recharge', 'recharge'),
)


# Create your models here.
class Coupon(models.Model):
    """
    优惠码模型
    """
    coupon_uuid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    coupon_code = models.CharField(max_length=MODULE_COUPON['COUPON_CODE_LEN'], unique=True)
    coupon_type = models.CharField(choices=COUPON_TYPE, max_length=20)
    coupon_value = models.IntegerField(validators=[positive])
    coupon_using_count = models.IntegerField(validators=[positive])
    coupon_using_user = models.IntegerField(validators=[positive])
    using_user_left = models.IntegerField()
    valid_datetime_start = models.DateTimeField()
    valid_datetime_end = models.DateTimeField()
    limit_lower = models.IntegerField(default=0)
    limit_upper = models.IntegerField(default=10000000)
    theme = models.CharField(blank=True, max_length=100)
    create_time = models.DateTimeField(auto_now_add=True)

    # is_valid = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode(self.coupon_uuid)


class CouponUser(models.Model):
    """
    优惠码用户关联模型
    """
    coupon_user_relate_uuid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    coupon_uuid = models.ForeignKey('Coupon', related_name='coupon_p')
    coupon_code = models.CharField(max_length=MODULE_COUPON['COUPON_CODE_LEN'])
    coupon_type = models.CharField(choices=COUPON_TYPE, max_length=20)
    coupon_value = models.IntegerField()
    user_uuid = models.CharField(max_length=50)
    payment_account_uuid = models.UUIDField()
    using_count_left = models.IntegerField()
    valid_datetime_start = models.DateTimeField()
    valid_datetime_end = models.DateTimeField()
    relate_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.coupon_user_relate_uuid)


# 使用类型:支付使用/充值使用
USAGE_SOURCE_TYPE = (
    ('payment', 'payment'),
    ('account', 'account'),
)


class CouponUsage(models.Model):
    """
    优惠码使用模型
    """
    coupon_usage_uuid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    coupon_uuid = models.ForeignKey('Coupon', related_name='coupon_t')
    coupon_code = models.CharField(max_length=MODULE_COUPON['COUPON_CODE_LEN'])
    user_uuid = models.CharField(max_length=50)
    payment_account_uuid = models.UUIDField()
    use_time = models.DateTimeField(auto_now_add=True)
    usage_source_type = models.CharField(choices=USAGE_SOURCE_TYPE, max_length=20)
    usage_source_uuid = models.UUIDField()

    def __unicode__(self):
        return unicode(self.coupon_usage_uuid)
