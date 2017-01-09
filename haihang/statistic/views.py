# -*- coding:utf-8 -*-

from statistic.models import HostStatistic, HostStatisticTest, HostStatisticPlus
from statistic.serializers import HostStatisticSerializer, HostStatisticTestSerializer, HostStatisticPlusSerializer
from rest_framework.decorators import api_view, list_route
from rest_framework.response import Response
from django.http import Http404, HttpResponse
from rest_framework import viewsets, mixins, status
from  bill.util import create_bill
import json
import logging
import datetime

log = logging.getLogger('statistic')


class StatisticViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    """
    queryset = HostStatistic.objects.all()
    serializer_class = HostStatisticSerializer

    @list_route(methods=['post'])
    def gain_statistic_byid(self, request):
        """
        通过容器id获取容器状态记录
        """
        try:
            if request.method == 'POST':
                host_uuid = request.data['host_uuid']
                statistic = HostStatistic.objects.filter(host_uuid=host_uuid)
                if statistic.count() > 0:
                    if statistic[0].host_status == 1:
                        host_starttime = statistic[0].host_starttime.replace(tzinfo=None)
                        statistic[0].host_status = 0
                        statistic[0].run_time += int((datetime.datetime.now() - host_starttime).seconds / 60)
                        serializer = HostStatisticSerializer(statistic[0])
                        return Response(serializer.data)
                    else:
                        serializer = HostStatisticSerializer(statistic[0])
                        return Response(serializer.data)
                else:
                    raise Http404('No %s matches the given query.' % statistic.model._meta.object_name)
        except KeyError:
            return Response({'detail': 'key error'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'badly formed hexadecimal UUID string'}, status=status.HTTP_400_BAD_REQUEST)


class StatisticPlusViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    """
    queryset = HostStatisticPlus.objects.all()
    serializer_class = HostStatisticPlusSerializer

    @list_route(methods=['post'])
    def gain_statistic_byid(self, request):
        """
        通过容器id获取容器状态记录
        """
        try:
            if request.method == 'POST':
                host_uuid = request.data['host_uuid']
                statistic = HostStatisticPlus.objects.filter(host_uuid=host_uuid)
                if statistic.count() > 0:
                    if statistic[0].host_status == 1:
                        host_lasttime = statistic[0].host_lasttime.replace(tzinfo=None)
                        statistic[0].host_status = 0
                        statistic[0].host_time += int((datetime.datetime.now() - host_lasttime).seconds / 60)
                        serializer = HostStatisticPlusSerializer(statistic[0])
                        return Response(serializer.data)
                    else:
                        serializer = HostStatisticPlusSerializer(statistic[0])
                        return Response(serializer.data)
                else:
                    raise Http404('No %s matches the given query.' % statistic.model._meta.object_name)
        except KeyError:
            return Response({'detail': 'key error'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'badly formed hexadecimal UUID string'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'])
    def change_statistic_status(self, request):
        """
        当容器状态发生改变时候，用于改变记录状态
        """
        # try:
        host_uuid = request.data['host_uuid']
        host_status = request.data['host_status']
        host_statistic = HostStatisticPlus.objects.filter(host_uuid=host_uuid)
        if host_statistic.count() > 0:
            # 由运行变成停止，记录运行时间
            if host_statistic[0].host_status == 1 and host_status == 0:
                host_lasttime = host_statistic[0].host_lasttime.replace(tzinfo=None)
                host_statistic[0].host_status = 0
                host_statistic[0].host_time += int((datetime.datetime.now() - host_lasttime).seconds / 60)
                host_statistic[0].host_lasttime = datetime.datetime.now()
                host_statistic[0].save()
                return Response({"detail": "change successful"})
            # 由停止改变成运行,改变最后一次启动时间
            elif host_status == 1 and host_statistic[0].host_status == 0:
                host_statistic[0].host_status = 1
                host_statistic[0].host_lasttime = datetime.datetime.now()
                host_statistic[0].save()
                return Response({"detail": "change successful"})
            # 容器删除，调用账单模块生成账单
            elif host_status == 2 and host_statistic[0].host_status != 2:
                host_statistic[0].host_status = 2
                host_statistic[0].save()
                my_status = create_bill(host_uuid=host_statistic[0].host_uuid, user_uuid=host_statistic[0].user_uuid, \
                                        cpumem_time=host_statistic[0].host_time,
                                        price_strategy=host_statistic[0].price_strategy, \
                                        host_starttime=host_statistic[0].host_starttime)
                if my_status is True:
                    return Response({"detail": "change successful"})
            else:
                # 如果两次状态没发生改变
                return Response({'no changed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('host_uuid is not exist.', status=status.HTTP_404_NOT_FOUND)
            # except KeyError:
            #     return Response({'detail': 'key error'}, status=status.HTTP_400_BAD_REQUEST)
            # except ValueError:
            #     return Response({'detail': 'badly formed hexadecimal UUID string'}, status=status.HTTP_400_BAD_REQUEST)
            # except:
            #     return Response({'detail': 'other error'}, status=status.HTTP_400_BAD_REQUEST)


class StatisticTestViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    """
    queryset = HostStatisticTest.objects.all()
    serializer_class = HostStatisticTestSerializer

    @list_route(methods=['get'])
    def get_rancher_data(self, request):
        print 'aa'
        account_id = request.GET.get('account_id', None)
        print account_id
        hosts = HostStatisticTest.objects.filter(account_id=account_id)
        serializer = HostStatisticTestSerializer(hosts, many=True)
        print len(serializer.data)
        return Response(serializer.data)


# 用于测试host_statistic接口获取数据
@api_view(['GET', 'POST'])
def con_user(request):
    datetime1 = datetime.datetime.now()
    print datetime1
    print 'test get host_statistic data。。。。。。'
    datalist = HostStatisticTest.objects.all()
    serializer = HostStatisticTestSerializer(datalist, many=True)
    print 'serializer used total time:', datetime.datetime.now() - datetime1
    print '- - - - - - - - - - - - -- - - - -- - - - - -- - - -- - - - -- - - -- - -- - - - - - -- - -- - -- - -  '
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def con_user1(request):
    datetime1 = datetime.datetime.now()
    print datetime1
    print 'test get json data'
    datalist = HostStatisticTest.objects.all()
    data = {}
    data['data'] = datalist
    print 'serializer1 used total time:', datetime.datetime.now() - datetime1
    print '--------------------------------------------------------------------------------------------------------'
    return HttpResponse(json.dumps(data), content_type='application/json')
