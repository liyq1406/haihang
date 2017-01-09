# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import uuid
from django.db import models
MONITOR_TYPE = (
    (1,'剩余额度'),
    (2,'剩余使用额度'),
)
NOTIFY_STRATEGY = (
    (1,'短信'),
    (2,'邮件'),
)


class AlertLevel(models.Model):
    """
    后台需要配置的参数,包括告警级别的设定，最低启动主机的标准
    """
    low = models.IntegerField(default=15)
    medium = models.IntegerField(default=7)
    high = models.IntegerField(default=3)
    #启动主机最低标准
    days = models.IntegerField(default=1)


#告警记录表
class AlertRecord(models.Model):
    user_id = models.CharField(max_length=100,verbose_name='用户id')
    alert_number  = models.IntegerField(verbose_name='告警次数',default=0)
    alert_time = models.DateTimeField(auto_now_add=True,verbose_name='告警时间')
    class Meta:
        ordering = ('alert_time',)
        verbose_name_plural = '告警记录表'


#测试用的用户账户表
class UserAccount(models.Model):
    useraccount_uuid = models.UUIDField(primary_key=True,default=uuid.uuid1)
    user_uuid = models.CharField(max_length=50,verbose_name='用户uuid')
    payment_account_uuid =models.UUIDField(verbose_name='账户uuid')

    class Meta:
        verbose_name_plural = '用户账户表(测试)'
    def __unicode__(self):
        return unicode(self.user_uuid)