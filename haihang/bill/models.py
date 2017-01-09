# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import uuid


# from django.contrib.auth.models import User
# Create your models here.


class Bill(models.Model):
    bill_uuid = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=True)
    bill_createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    host_uuid = models.UUIDField(verbose_name='主机uuid')
    name = models.CharField(max_length=50,blank=True,verbose_name='主机名称')
    user_uuid = models.CharField(max_length=50, verbose_name='用户id')
    run_time = models.FloatField(verbose_name='主机运行时长(min)', blank=True, default=0)
    total_fee = models.FloatField(verbose_name='总费用', default=0)
    pay_status = models.BooleanField(default=False, verbose_name='是否已经支付')
    # 如果一个主机需要结算，则需生成新账单，则旧账单记录状态标记为False;当账单支付成功后，记录状态也要改为False
    bill_status = models.BooleanField(default=True, verbose_name='记录状态')
    existed = models.BooleanField(default=True, verbose_name='是否显示')
    month = models.IntegerField(blank=True, null=True, verbose_name='账单月份')
    bill_account_time = models.DateTimeField(blank=True, null=True, verbose_name='账单结算日期')

    # owner = models.ForeignKey('auth.User',related_name='bills')
    class Meta:
        ordering = ('bill_createtime',)
        verbose_name_plural = '账单表'

    def __unicode__(self):
        return unicode(self.bill_uuid)


class BillRecord(models.Model):
    host_uuid = models.UUIDField(verbose_name='主机uuid')
    lifetime = models.FloatField()
    cpu = models.IntegerField()
    mem = models.IntegerField()
    name = models.CharField(max_length=50, blank=True, null=True)
    disk = models.IntegerField()


class MonthAccountRecord(models.Model):
    """
    记录月账单生成失败的 用户
    失败的 原因主要是由于网络延迟，从beancounter获取数据失败
    """
    user_id = models.CharField(max_length=50)
    month = models.IntegerField()
    pay_status = models.BooleanField(default=False)
    create_time = models.DateTimeField(blank=True, auto_now_add=True)

