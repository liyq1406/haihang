# -*- coding:utf-8 -*-
from statistic.models import HostStatistic,HostStatisticPlus
from statistic.models import HostUser

def get_statistic_byhost(host_uuid):
    jqueryset = HostStatistic.objects.filter(host_uuid=host_uuid)
    return jqueryset

def get_all_hoststatistic():
    """
    获取所有的监控容器
    :return:
    """
    jqueryset = HostStatistic.objects.all()
    return jqueryset

def get_al1_hoststatistic_plus():
    """
    获取所有的监控容器
    :return:
    """
    jqueryset = HostStatisticPlus.objects.all()
    return jqueryset

def get_statistic_byhostuuid(host_uuid):
    """
    通过host_uuid获取监控的容器记录
    """
    statistic = HostStatistic.objects.filter(host_uuid=host_uuid)
    return statistic
def get_statistic_byuserid(usre_uuid):
    """
    通过user_uuid获取监控的容器记录
    """
    statistic = HostStatistic.objects.filter(user_uuid=user_uuid)
    return statistic


def get_host_user(user_uuid):
    """
    通过user_uuid获取该用户的所有计量统计列表

    """
    try:
        host_statistic = HostStatistic.objects.filter(user_uuid=user_uuid)
        return host_statistic
    except ValueError:
        return []

