# # -*- coding:utf-8 -*-
#
# from Payment.initConf import ENV_INIT
# from bill.util import create_bill
# from models import HostStatistic, HostUser, HostStatisticTest
# from module_payment_account.models import PaymentAccount
# from monitor.models import AlertLevel
# from random import Random
# import datetime
# import json
# import logging
# import pytz
# import redis
# import requests
# import uuid
# log = logging.getLogger('payment')
#
# def random_str(randomlength=8):
#     str = ''
#     chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
#     length = len(chars) - 1
#     random = Random()
#     for i in range(randomlength):
#         str+=chars[random.randint(0, length)]
#     return str
# #生成测试数据
# def create_test_data():
#     alert = AlertLevel()
#     alert.save()
#     for one in range(10):
#         id1 = random_str(randomlength=8)
#         payment = PaymentAccount()
#         payment.user_uuid=id1
#         payment.balance = 500
#         payment.save()
#         test_statistic = HostStatisticTest()
#         test_statistic.host_uuid = uuid.uuid1()
#         test_statistic.account_id = id1
#         test_statistic.cpu=1
#         test_statistic.mem = 1024
#         test_statistic.disk = 500
#         test_statistic.lifetime = 10457
#         test_statistic.save()
#
#
# def host_statistic():
#     """
#     计量统计方案一：每分钟从rancher获取容器运行状态，并保存
#
#     """
#     print 'statistic time1:',datetime.datetime.now()
#     # user_info = urllib.urlopen("http://120.24.62.88:8007/con_user/").read()
#     # # 反序列化成为字典类型
#     # stream = BytesIO(user_info)
#     # data = JSONParser().parse(stream)
#     user_info = requests.get('http://120.24.62.88:8007/con_user/')
#     data = json.loads(user_info.text)
#     print 'statistic time2:',datetime.datetime.now()
#     if len(data)>0:
#         for one in data:
#             host_object = HostStatistic.objects.filter(host_uuid=one['host_uuid']).\
#                 filter(user_uuid=one['user_uuid'])
#             #当该容器计量统计存在
#             if len(host_object)>0:
#                 # #容器由运行变成停止,需要统计运行时间
#                 # if host_object[0].host_status==1 and one['host_status']==0:
#                 #     host_lasttime = host_object[0].host_lasttime.replace(tzinfo=None)
#                 #     host_object[0].host_status = 0
#                 #     host_object[0].host_time +=int((datetime.datetime.now()-host_lasttime).seconds/60)
#                 #     host_object[0].host_lasttime = datetime.datetime.now(pytz.timezone('UTC'))
#                 #     host_object[0].save()
#                 #     log.info("[statistic] the host:%s from runnging to stopped",host_object[0].host_uuid)
#                 # #容器由停止变成运行，需要把当前时间定为最后一次启动时间
#                 # elif host_object[0].host_status==0 and one['host_status']==1:
#                 #     host_object[0].host_status = 1
#                 #     host_object[0].host_lasttime = datetime.datetime.now(pytz.timezone('UTC'))
#                 #     host_object[0].save()
#                 #     log.info("[statistic] the host:%s from stop to running", host_object[0].host_uuid)
#                 # #容器容器由停止变成删除，需要结算账单
#                 # elif host_object[0].host_status==0 and one['host_status']==2:
#                 #     host_object[0].host_status = 2
#                 #     host_object[0].record_status=False
#                 #     host_object[0].save()
#                 #     log.info("[statistic] the host:%s from stop to deleted", host_object[0].host_uuid)
#                 #     if account_bill(host_uuid=one['host_uuid'])==True:
#                 #         log.info("[statistic] the host:%s\'s bill has been accounted",host_object[0].host_uuid)
#                 #     else:
#                 #         log.error("[statistic] the host:%s account bill failed!",host_object[0].host_uuid)
#                 #容器由运行变成删除，1.需要统计运行时间，2结算账单
#                 if  host_object[0].host_status==1 and one['host_status']==0:
#                     host_lasttime = host_object[0].host_lasttime.replace(tzinfo=None)
#                     host_object[0].run_time +=int((datetime.datetime.now()-host_lasttime).seconds/60)
#                     host_object[0].host_lasttime = datetime.datetime.now(pytz.timezone('UTC'))
#                     host_object[0].host_status = 2
#                     host_object[0].record_status=False
#                     host_object[0].save()
#                     log.info("[statistic] the host:%s from running to deleted", host_object[0].host_uuid)
#                     if account_bill(host_uuid=one['host_uuid']) is True:
#                         log.info("[statistic] the host:%s\'s bill has been accounted",host_object[0].host_uuid)
#                     else:
#                         log.error("[statistic] the host:%s account bill failed!",host_object[0].host_uuid)
#                 else:
#                     pass
#             #当计量统计不存在:1.需要生成，2.创建账单,3.记录容器与用户的关系
#             else:
#                 statistic = HostStatistic()
#                 statistic.host_uuid = one['host_uuid']
#                 statistic.user_uuid = one['user_uuid']
#                 #statistic.host_status = one['host_status']
#                 statistic.host_starttime = one['host_starttime']
#                 statistic.host_cpu = one['host_cpu']
#                 statistic.host_mem = one['host_mem']
#                 statistic.host_disk = one['host_disk']
#                 statistic.price_strategy = one['price_strategy']
#                 statistic.host_net = one['host_net']
#                 statistic.host_lasttime = one['host_lasttime']
#                 statistic.save()
#                 #
#                 user_host = hostUser()
#                 user_host.host_uuid=one['host_uuid']
#                 user_host.user_uuid = one['user_uuid']
#                 user_host.save()
#                 status = create_bill(user_uuid=one['user_uuid'],host_uuid=one['host_uuid']\
#                                          ,cpumem_time=one['run_time'],price_strategy=one['price_strategy'], \
#                                          host_starttime=one['host_starttime'])
#                 if status != True:
#                     log.error('[statistic] create a new bill failed')
#
#     else:
#         log.error('[statistic] the rancher\'s data is none')
#     print 'statistic time3:',datetime.datetime.now()
#
#
# def host_statistic1():
#     """
#     计量统计方案一：每分钟从rancher获取容器运行状态，并保存
#
#     """
#     print 'start statistic:',datetime.datetime.now()
#     r = redis.Redis(host=ENV_INIT['REDIS_HOST'],port=ENV_INIT['REDIS_PORT'],db=ENV_INIT['REDIS_DB'])
#     time1 = datetime.datetime.now()
#     # user_info = requests.get('http://120.24.62.88:8007/con_user/')
#     try:
#         user_info = requests.get(ENV_INIT['RANCHER_URL'])
#         data =user_info.json()
#         if len(data)>0:
#             for one in data:
#                 last_status = r.get(one['host_uuid'])
#                 if last_status is None:
#                     statistic = HostStatistic()
#                     statistic.host_uuid = one['host_uuid']
#                     statistic.user_uuid = one['user_uuid']
#                     # statistic.host_status = one['host_status']
#                     statistic.host_starttime = one['host_starttime']
#                     statistic.host_cpu = one['host_cpu']
#                     statistic.host_mem = one['host_mem']
#                     statistic.host_disk = one['host_disk']
#                     statistic.host_net = one['host_net']
#                     statistic.save()
#                     # 写入redis
#                     r.set(one['host_uuid'], 1)
#                     user_host = HostUser()
#                     user_host.host_uuid = one['host_uuid']
#                     user_host.user_uuid = one['user_uuid']
#                     user_host.save()
#                     status = create_bill(user_uuid=one['user_uuid'],host_uuid=one['host_uuid'], run_time=one['run_time'])
#                     if status != True:
#                         log.error('[statistic] create a new bill failed')
#
#                 elif int(last_status)==1 and one['host_status']==0:
#                     host_object = HostStatistic.objects.get(host_uuid=one['host_uuid'])
#                     host_starttime = host_object.host_starttime.replace(tzinfo=None)
#                     host_object.run_time = int((datetime.datetime.now()-host_starttime).seconds/60)
#                     host_object.host_status = 0
#                     host_object.record_status=False
#                     host_object.save()
#                     r.set(one['host_uuid'], 0)
#                     log.info("[statistic] the host:%s from running to stop", host_object.host_uuid)
#                     if account_bill(host_uuid=one['host_uuid'])==True:
#                         log.info("[statistic] the host:%s\'s bill has been accounted",host_object.host_uuid)
#                     else:
#                         log.error("[statistic] the host:%s account bill failed!",host_object.host_uuid)
#                 else:
#                     pass
#
#         else:
#             log.error('[statistic] the rancher\'s data is none')
#         print 'statistic end:',datetime.datetime.now()
#         print 'total time:',datetime.datetime.now()-time1
#     except ValueError:
#         log.error('[statistic] the rancher has no JSON object could be decoded')
#
#
#
#
