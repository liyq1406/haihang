# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models

STATUS_CHOICE = (
    (0,'stop'),
    (1,'runing')
)



class HostStatistic(models.Model):
    """
    主机状态记录表(方案一）
    """
    created=models.DateTimeField(max_length=50,auto_now_add=True,verbose_name='生成日期')
    host_uuid = models.CharField(max_length=50,verbose_name='容器uuid')
    user_uuid = models.CharField(max_length=50, verbose_name='用户id', blank=True)
    host_status = models.IntegerField(choices=STATUS_CHOICE,default=1,verbose_name='容器运行装态(运行中/停止')
    host_starttime = models.DateTimeField(verbose_name='容器启动时间')
    host_cpu = models.IntegerField(verbose_name='容器cpu(核)')
    host_mem = models.IntegerField(verbose_name='容器mem(MB)')
    host_disk = models.IntegerField(verbose_name='容器disk(MB)')
    host_net = models.CharField(max_length=50,default='Free',verbose_name='容器网络')
    run_time = models.IntegerField(verbose_name='容器运行时间',default=0)
    record_status = models.BooleanField(default=True,verbose_name='记录状态')
    class Meta:
        ordering = ('created',)
        verbose_name_plural = '容器记录表'
    def __unicode__(self):
        return unicode(self.host_uuid)

class HostStatisticPlus(models.Model):
    """
    主机状态记录表(方案二)
    """
    created=models.DateTimeField(auto_now_add=True,verbose_name='生成日期')
    host_uuid = models.UUIDField(verbose_name='容器uuid')
    user_uuid = models.CharField(max_length=50,verbose_name='用户id')
    host_status = models.IntegerField(choices=STATUS_CHOICE,default=1,verbose_name='容器运行状态(运行中/停止/删除')
    host_starttime = models.DateTimeField(verbose_name='容器启动时间')
    host_cpu = models.IntegerField(verbose_name='容器cpu(核)')
    host_mem = models.IntegerField(verbose_name='容器mem(MB)')
    host_disk = models.IntegerField(verbose_name='容器disk(MB)')
    host_net = models.CharField(max_length=50,default='Free',verbose_name='容器网络')
    host_time = models.IntegerField(verbose_name='容器运行时间',default=0)
    record_status = models.BooleanField(default=True,verbose_name='记录状态')
    class Meta:
        ordering = ('created',)
        verbose_name_plural = '容器记录表plus'
    def __unicode__(self):
        return unicode(self.host_uuid)

class HostStatisticTest(models.Model):
    created=models.DateTimeField(auto_now_add=True,verbose_name='生成日期')
    host_uuid = models.UUIDField(verbose_name='容器uuid',editable=True)
    account_id = models.CharField(max_length=50,verbose_name='用户id')
    cpu = models.IntegerField(verbose_name='容器cpu(核)')
    mem = models.IntegerField(verbose_name='容器mem(MB)')
    disk = models.IntegerField(verbose_name='容器disk(MB)')
    net = models.CharField(max_length=50,default='Free',verbose_name='容器网络')
    lifetime = models.IntegerField(verbose_name='容器运行时间',default=0)
    class Meta:
        ordering = ('created',)
        verbose_name_plural = '容器记录表(测试)'



class HostUser(models.Model):
    created = models.DateTimeField(max_length=50, auto_now_add=True, verbose_name='生成日期')
    host_uuid = models.UUIDField(verbose_name='容器uuid')
    user_uuid = models.UUIDField(max_length=50, verbose_name='用户id', blank=True)
    class Meta:
        ordering = ('created',)
        verbose_name_plural = '容器与用户'

    def __unicode__(self):
        return unicode(self.user_uuid)

