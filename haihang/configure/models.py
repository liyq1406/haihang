# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


CACHE_VERSION = 'configure'


class Configure(models.Model):
    """
    # 存储通用配置
    """
    group_id = models.IntegerField(default=0, verbose_name='配置项分租ID')
    code = models.CharField(max_length=128, unique=True, verbose_name='配置项唯一key')
    data_range = models.CharField(max_length=128, verbose_name='数据取值范围')
    data_type = models.CharField(max_length=32, default='string', verbose_name='数据类型')
    value = models.TextField(verbose_name='配置项的值')
    sort_order = models.IntegerField(default=1, verbose_name='配置项展示排序的序号')
    remark = models.CharField(max_length=128, verbose_name='配置项描述')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建或修改时间')
