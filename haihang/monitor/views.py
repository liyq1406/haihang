# -*- coding:utf-8 -*-
from serializers import AlertRecordSerializer
from rest_framework import viewsets, status
from models import AlertRecord
from rest_framework.response import Response
from rest_framework.decorators import list_route
from monitor.util import reckon_remaind
from price.util import gain_price_byuuid
from Payment.util import get_config_value
import logging
from Payment.disable import CsrfExemptSessionAuthentication, auth_required
log = logging.getLogger('payment')


class AccountMonitorViewSet(viewsets.GenericViewSet):
    """
    对外提供：create,partial_update,get_monitor接口
    """
    queryset = AlertRecord.objects.all()
    serializer_class = AlertRecordSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @auth_required(role='user')
    @list_route(methods=['post'])
    def check_account(self, request):
        """
        检查账户余额
        :param request:
        :return:
        """
        try:
            payment_accountid = request.data['payment_accountid']
            price_uuid = request.data['price_uuid']
            num = request.data['num']
        except KeyError:
            return Response({'detail': 'the key is not enough or error'}, status=status.HTTP_400_BAD_REQUEST)
        # print 'type(price_uuid):',type(price_uuid)
        price = gain_price_byuuid(price_uuid=price_uuid)
        if price:
            dict1 = {}
            # 估算余额可以支持使用的时长
            try:
                days_dic = reckon_remaind(payment_accountid, num, price.price)
                if days_dic['last_days'] < int(get_config_value('min_remaining_days')):
                    dict1['is_allow'] = False
                else:
                    dict1['is_allow'] = True

                dict1['last_days'] = days_dic['last_days']
                dict1['active_money'] = days_dic['active_money']
                return Response(dict1, status=status.HTTP_200_OK)
            except Exception as e:
                log.error('[monitor] {}'.format(e.__str__()))
                return Response({'detail': 'server error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': 'the price strategy is not existed'}, status.HTTP_400_BAD_REQUEST)