# -*- coding:utf-8 -*-
from django.db import models
import uuid


# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Price(models.Model):
    created = models.DateTimeField(max_length=50, auto_now_add=True, verbose_name='生成日期')
    price_uuid = models.UUIDField(primary_key=True, default=uuid.uuid1)
    cpu = models.IntegerField(verbose_name='cpu(核数)')
    mem = models.IntegerField(verbose_name='内存(MB)')
    disk = models.IntegerField(verbose_name='磁盘(GB)')
    net = models.CharField(max_length=20, default='FREE')
    price = models.FloatField(verbose_name='定价(分/分钟)')
    host_model = models.CharField(max_length=20, verbose_name='主机规格', blank=True)
    # 是否显示
    is_existed = models.BooleanField(default=True)
    effective_date = models.DateField(verbose_name='生效日期')
# 是否是最新的定价
# is_new = models.BooleanField(default=True)


class PriceAddRecord(models.Model):
    """
    价格修改记录表
    """
    price_uuid = models.UUIDField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
