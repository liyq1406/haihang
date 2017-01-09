# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from Payment.initConf import MODULE_PAYMENT_ACCOUNT
# from Payment.util import get_config_value
from Payment.validates import non_negative, is_digit
import uuid

# 变更来源:支付单(充值)/账单(扣费)/优惠码使用(充值)
MODIFY_SOURCE_TYPE = (
    ('payment', 'payment'),
    ('refund', 'refund'),
    ('bill', 'bill'),
    # ('coupon_usage', 'coupon_usage'),
    ('admin', 'admin'),
)
# Create your models here.

class PaymentAccount(models.Model):
    """
    支付账户模型
    """
    payment_account_uuid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
    user_uuid = models.CharField(max_length=50, unique=True, validators=[is_digit])
    is_valid = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    credit = models.FloatField(validators=[non_negative])
    balance = models.FloatField(default=MODULE_PAYMENT_ACCOUNT['BALANCE'])
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.payment_account_uuid)


class AccountRecord(models.Model):
    """
    账户变更记录模型
    """
    account_record_uuid = models.UUIDField(primary_key=True ,default=uuid.uuid1, editable=False)
    payment_account_uuid = models.ForeignKey('PaymentAccount', related_name='paymentAccount')
    modify_balance = models.FloatField()
    modify_source_type = models.CharField(choices=MODIFY_SOURCE_TYPE, max_length=50)
    modify_source_uuid = models.CharField(blank=True, max_length=36)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.account_record_uuid)

    # class Meta:
    #     ordering = ('-create_time',)

