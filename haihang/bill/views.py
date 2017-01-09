# -*- coding:utf-8 -*-
from Payment.util import get_kwargs, get_query_paganaiton
from bill.models import Bill
from bill.serializers import BillSerializer
from bill.util import create_url, get_record_bill
from django.http import HttpResponse
from django.core.cache import cache
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from util import check_host_bill
import datetime
import logging
import requests
from Payment.disable import CsrfExemptSessionAuthentication, auth_required


log = logging.getLogger('payment')
BILL_CACHE_VERSION = 'bill'


def get_host_info_from_cache(user_id):
    if user_id is None or user_id in ['undefined', 'null']:
        return None
    key = 'bean_counter_host_info_%s' % (user_id)
    v = cache.get(key, version=BILL_CACHE_VERSION)
    if v is not None:
        log.debug('get host info [%s] from cache' % (user_id))
        return v

    log.debug('get host info [%s] from beancounter' % (user_id))
    host_url = create_url('1a' + user_id)
    try:
        hosts_all = requests.get(host_url, timeout=2).json()
        cache.set(key, hosts_all, 10, version=BILL_CACHE_VERSION)
        return hosts_all
    except Exception, e:
        log.error('get host info [%s] from beancounter except[%s]' % (user_id, str(e)))
        return None


def update_host_bill(user_id):
    """
    通过用户id来更新账单
    :param user_id:
    :return:
    """

    hosts_all = get_host_info_from_cache(user_id)
    if hosts_all and isinstance(hosts_all, dict):
        hosts = hosts_all.get('hosts', [])
        user_name = hosts_all.get('id', '')
        user_name = user_name[2:] if user_name else ''
        for host in hosts:
            try:
                check_host_bill(host=host, user_name=user_name, choice='user')
            except Exception as e:
                # traceback.print_stack()
                log.error('[bill] update_host_bill {}'.format(e.__str__()))


class BillViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取所有账单
    """
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @auth_required(role='admin')
    @list_route(methods=['get'])
    def get_bills_bycondition(self, request):
        """
        后台根据条件产看账单
        :param request:
        :return:
        """
        query_param = {
            'bill_uuid': request.GET.get('bill_uuid', None),
            'user_uuid': request.GET.get('user_uuid', None),
            'host_uuid': request.GET.get('host_uuid', None),
            'pay_status': request.GET.get('pay_status', None),
            'bill_account_time__gte': request.GET.get('bill_account_time__gte', None),
            'bill_account_time__lte': request.GET.get('bill_account_time__lte', None)
        }

        try:
            total_bills = Bill.objects.filter(**get_kwargs(query_param))
            count = total_bills.count()
            desc, limit, offset = get_query_paganaiton(request)
            bills = total_bills.order_by('bill_account_time')[offset:offset + limit]
            serializer = BillSerializer(bills, many=True)
            return Response({'content': serializer.data, 'count': count})
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '5400'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'content': {}, 'count': 0})
        except Exception as e:
            log.error('[bill] views.get_bills_bycondition.e:{}'.format(e.__str__()))
            return Response({'detail:': 'value has an invalid format', 'error_code': '5400'},
                            status=status.HTTP_400_BAD_REQUEST)

    @auth_required(role='user')
    @list_route(methods=['get'])
    def get_year_fee(self, request):
        """
        用户获取年度总费用，已经结算
        :param request:
        :return:
        """
        try:
            user_uuid = request.GET.get('user_uuid')
            update_host_bill(user_id=user_uuid)
            year = datetime.datetime.now().strftime("%Y")
            str_date = year + '-01-01T00:00:00.00Z'
            year_first_day = datetime.datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=None)
            print 'year_first_day:', year_first_day
            bills = Bill.objects.filter(user_uuid=user_uuid, bill_createtime__gte=year_first_day)
            total_fee = 0
            for one in bills:
                total_fee += one.total_fee

            return Response({'total_fee': total_fee})
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '5400'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'total_fee': 0})
        except Exception as e:
            log.error('[bill] views.get_year_fee.e:{}'.format(e.__str__()))
            return Response({'detail:': 'server  error', 'error_code': '5500'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @auth_required(role='user')
    @list_route(methods=['get'])
    def get_current_monthbill(self, request):
        """
        用户获取当前月份账单（包括支付的月账单和未结算的那部分费用）
        :param request:
        :return:
        """
        try:
            user_uuid = request.GET.get('user_uuid')
            update_host_bill(user_id=user_uuid)

            month = int(datetime.datetime.now().strftime("%m"))
            bills = Bill.objects.filter(user_uuid=user_uuid, month=month)
            host_list = []
            hostid_list = []
            for bill in bills:
                hostid_list.append(bill.host_uuid)
            hostid_set = set(hostid_list)
            all_hosts_fee = 0
            for hostid in hostid_set:
                host_bill = bills.filter(host_uuid=hostid)
                total_fee = 0
                info = {}
                for one in host_bill:
                    total_fee += one.total_fee
                record_bill = get_record_bill(host_uuid=str(hostid),name='',cpu=0, mem=0, disk=0)
                info['uuid'] = hostid
                info['cpu'] = record_bill.cpu
                info['disk'] = record_bill.disk
                info['mem'] = record_bill.mem
                info['fee'] = total_fee
                info['name'] = record_bill.name
                host_list.append(info)
                all_hosts_fee += total_fee
            return Response({'total_fee': all_hosts_fee, 'host_list': host_list})
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '5400'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'badly formed hexadecimal UUID string',
                             'error_code': '5400'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log.error('[bill] views.get_current_monthbill.e:{}'.format(e.__str__()))
            return Response({'detail:': 'server  error', 'error_code': '5500'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @auth_required(role='user')
    @list_route(methods=['get'])
    def getbill_bytime(self, request):
        """
        用户根据时间查询账单
        :param request:
        :return:
        """
        try:
            user_uuid = request.GET.get('user_uuid', None)
            datetime1 = request.GET.get('datetime1', None)
            datetime2 = request.GET.get('datetime2', None)
            bills = Bill.objects.filter(user_uuid=user_uuid, existed=True, bill_createtime__gte=datetime1, \
                                        bill_createtime__lte=datetime2)
            host_list = []
            hostid_list = []
            for bill in bills:
                hostid_list.append(bill.host_uuid)
            hostid_set = set(hostid_list)
            all_hosts_fee = 0
            hostid_set = list(hostid_set)
            for hostid in hostid_set:
                host_bill = bills.filter(host_uuid=hostid)
                total_fee = 0
                info = {}
                for one in host_bill:
                    total_fee += one.total_fee
                record_bill = get_record_bill(host_uuid=str(hostid),name='',cpu=0, mem=0, disk=0)
                info['uuid'] = hostid
                info['cpu'] = record_bill.cpu
                info['disk'] = record_bill.disk
                info['mem'] = record_bill.mem
                info['fee'] = total_fee
                info['name'] = record_bill.name
                host_list.append(info)
                all_hosts_fee += total_fee
            return Response({'host_list': host_list, 'total_fee': all_hosts_fee})
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '5400'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'badly formed hexadecimal UUID string',
                             'error_code': '5400'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log.error('[bill] views.getbill_bytime.e:{}'.format(e.__str__()))
            return Response({'detail:': 'server  error', 'error_code': '5500'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def display_meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))
