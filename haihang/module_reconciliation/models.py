# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from django.db import models
import uuid

# 处理状态
DEAL_STATUS = (
    ('open', 'open'),
    ('close', 'close'),
)

# 对账错误分为 记录缺失, 记录多余, 金额异常以及状态异常
ERROR_TYPE = (
    ('miss', 'miss'),
    ('multi', 'multi'),    
    ('amount', 'amount'),    
    ('status', 'status'),    
)

# Create your models here.
class Reconciliation(models.Model):
    reconciliation_uuid = models.UUIDField(default=uuid.uuid1, primary_key=True, editable=False)
    payment_no = models.CharField(blank=True, max_length=50, null=True)
    error_type = models.CharField(max_length=60)
    payment_record = models.TextField(blank=True)
    third_record = models.TextField()
    deal_result = models.TextField(blank=True)
    deal_status = models.CharField(max_length=10, choices=DEAL_STATUS, default='open')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return unicode(self.reconciliation_uuid)

    class Meta:
        ordering = ('-create_time',)
        