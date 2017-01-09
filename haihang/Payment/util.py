# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals
from Payment.initConf import MODULE_PAGANITION
from configure import models
from configure.models import CACHE_VERSION
from django.core.cache import cache

def get_kwargs(data={}):
    kwargs = {}
    for (k , v)  in data.items() :
        if v:
            kwargs[k] = v          
    return kwargs

def gen_dict(param, **kwargs):
    for k in kwargs:
        param[k] = kwargs[k]
    return param

def get_query_paganaiton(request):
    desc = '-' if request.GET.get('desc', MODULE_PAGANITION['DESC'])=='1' else ''
    limit = int(request.GET.get('limit', MODULE_PAGANITION['LIMIT']))
    offset = int(request.GET.get('offset', MODULE_PAGANITION['OFFSET']))
    return desc, limit, offset


def load_config_data():
    data = models.Configure.objects.all()
    for item in data:
        try:
            if item.data_type == 'int':
                cache.set(item.code, int(item.value), version=CACHE_VERSION)
            elif item.data_type == 'float':
                cache.set(item.code, float(item.value), version=CACHE_VERSION)
            elif item.data_type == 'bool':
                if item.value in ['', None, 0,'0','false',False,'False','N']:
                    cache.set(item.code, False, version=CACHE_VERSION)
                else:
                    cache.set(item.code, True, version=CACHE_VERSION)
            else:
                cache.set(item.code, str(item.value), version=CACHE_VERSION)
        except:
            pass

def get_config_value(key, default=''):
    v = cache.get(key, version=CACHE_VERSION)
    if v is not None:
        return v
    
    load_config_data()
    return cache.get(key, default, version=CACHE_VERSION)

        


