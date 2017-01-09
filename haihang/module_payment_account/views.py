# -*- coding:utf-8 -*-
 
import logging
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from module_payment_account.serializers import PaymentAccountRetrieveSerializer
from module_payment_account.serializers import PaymentAccountListCreateSerializer
from module_payment_account.serializers import AccountRecordSerializer
from module_payment_account.models import PaymentAccount, AccountRecord
from Payment.initConf import MODULE_PAYMENT_ACCOUNT
from Payment.util import get_config_value
from Payment.util import get_query_paganaiton, get_kwargs
from Payment.disable import CsrfExemptSessionAuthentication, auth_required
from interface import is_valid_user_uuid

log = logging.getLogger('payment')

class PaymentAccountViewSet(viewsets.GenericViewSet):
    queryset = PaymentAccount.objects.all()
    serializer_class = PaymentAccountListCreateSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @auth_required(role='superadmin')
    def create(self, request):
        '''
        新建账户
        '''
        serializer = PaymentAccountListCreateSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'detail': '参数错误',
                'error_code': '2400'
            },status=status.HTTP_400_BAD_REQUEST)

    @auth_required(role='admin')
    def list(self, request):
        '''
        # 账户列表
        '''
        # 过滤
        query_param = {
            'payment_account_uuid': request.GET.get('payment_account_uuid', None),
            'is_valid': request.GET.get('is_valid', None),
            'user_uuid': request.GET.get('user_uuid', None),
            'balance__gte': request.GET.get('balance__gte', None),
            'balance__lte': request.GET.get('balance__lte', None),
            'credit__gte': request.GET.get('credit__gte', None),
            'credit__lte': request.GET.get('credit__lte', None),
        }
        try:
            records = PaymentAccount.objects.filter(**get_kwargs(query_param))
            count = records.count()
        except ValueError:
            log.error('[account] list account error, queryParams: %s', str(query_param))
            return Response({
                'detail': '参数错误',
                'error_code': '1400'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 排序分页
        desc, limit, offset = get_query_paganaiton(request)
        queryset = records.order_by(desc + 'create_time')[offset:offset+limit]
        serializer = PaymentAccountListCreateSerializer(queryset, many=True)
        return Response({'count':count,'content':serializer.data})

    @auth_required(role='user')
    def retrieve(self, request, pk=None):
        '''
        # 获取指定账户详情
        '''
        queryset = PaymentAccount.objects.all()
        try:
            paymentAccount = get_object_or_404(queryset, pk=pk)
        except ValueError:
            log.error('[account] get account info error, pk: %s', pk)
            return Response({
                'detail': '参数错误',
                'error_code': '1400'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = PaymentAccountRetrieveSerializer(paymentAccount, context={'request': request})
        return Response(serializer.data)

    """
    def update(self, request, pk=None):
        '''
        # 账户变更接口, 变更用户额度以及可用性
        {
            "modify_balance":-100,
            "modify_source_type": "bill",
            "modify_source_uuid":"68c4add4-9f14-11e6-80d3-6451066036bd"
        }
        '''
        queryset = PaymentAccount.objects.all()
        try:
            paymentAccount = get_object_or_404(queryset, pk=pk)
        except ValueError:
            #return Response({'detail': 'UUID validate fail'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PaymentAccountUpdateSerializer(paymentAccount, data=request.data, context={'request': request})
        if serializer.is_valid():
            # 基于策略以及额度判断 
            if get_config_value('strategy', 'NO_BALANCE_LEFT') == 'NO_BALANCE_LEFT':
                balance = paymentAccount.balance + request.data['modify_balance']
                is_valid = False if balance < 0 else True

            if get_config_value('strategy', 'NO_BALANCE_LEFT') == 'NO_CREDIT_LEFT':
                balance = paymentAccount.balance + request.data['modify_balance']
                is_valid = False if (balance + paymentAccount.credit) < 0 else True

            accountRecord = AccountRecord(payment_account_uuid=paymentAccount,
                                         modify_balance=request.data['modify_balance'],
                                         modify_source_type=request.data['modify_source_type'],
                                         modify_source_uuid=request.data['modify_source_uuid'])
            try:
                # 用户额度变更
                serializer.save(account_record_uuid=accountRecord.account_record_uuid, balance=balance, is_valid=is_valid)
                # 变更记录生成
                accountRecord.save()
                log.info('[account] change balance from modify_source_uuid %s success', request.data['modify_source_uuid'])
                return Response(serializer.data)
            except TransactionManagementError:
                log.error('[account] change balance from modify_source_uuid %s error', request.data['modify_source_uuid'])
                return Response({'error':u'Mysql error'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    """
    
    @auth_required(role='superadmin')
    def partial_update(self, request, pk=None):
        '''
        # 账户修改接口, 修改账户基本信息.
        '''
        queryset = PaymentAccount.objects.all()
        try:
            paymentAccount = get_object_or_404(queryset, pk=pk)
            if request.data.get('user_uuid') and request.data.get('user_uuid') != paymentAccount.user_uuid:
                return Response({
                    'detail': '用户envId不能变更',
                    'error_code': '1400'
                }, status=status.HTTP_400_BAD_REQUEST)  
            old_balance = paymentAccount.balance
            serializer = PaymentAccountListCreateSerializer(
                            paymentAccount, 
                            data=request.data,
                            partial=True, 
                            context={'request': request})
        except ValueError:
            log.error('[account] modify account error, pk: %s', pk)
            return Response({
                'detail': '参数错误',
                'error_code': '1400'
            }, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            new_balance = request.data.get('balance')
            accountRecord = AccountRecord(
                                payment_account_uuid=paymentAccount,
                                modify_balance=new_balance - old_balance,
                                modify_source_type='admin')
            accountRecord.save()
            log.info('[account] admin update payment_account_uuid %s, balance: %f, credit: %f', 
                     pk, new_balance, request.data.get('credit'))
            return Response(serializer.data)
        else:
            log.error('[account] modify account error, pk: %s', pk)
            return Response({
                'detail': '参数错误',
                'error_code': '1400'
            }, status=status.HTTP_400_BAD_REQUEST)


class PaymentUserViewSet(viewsets.GenericViewSet):
    queryset = PaymentAccount.objects.all()
    serializer_class = PaymentAccountRetrieveSerializer 

    @auth_required(role='user')   
    def list(self, request):
        '''
        # 使用user_uuid查询账户详情, user_uuid不存在时使用该uuid以及默认配置创建新账户
        '''
        pk = request.GET.get('user_uuid')
        if not is_valid_user_uuid(pk):
            return Response({
                'detail': 'user_uuid非法',
                'error_code': '2400'
            }, status=status.HTTP_400_BAD_REQUEST)  
        try:
            queryset = PaymentAccount.objects.get(user_uuid=pk)
        except PaymentAccount.DoesNotExist:
            # 查询不到该用户时使用默认配置创建新账号
            queryset = PaymentAccount(user_uuid=pk, credit=get_config_value('credit', 0))
            queryset.save()
            log.info('[account] create payment account %s use default settings.', pk)
        except ValueError:
            log.error('[account] get account info error, user_uuid: %s', pk)
            return Response({
                'detail': '参数错误',
                'error_code': '1400'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = PaymentAccountRetrieveSerializer(queryset, context={'request': request})
        return Response(serializer.data)


class AccountRecordViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = AccountRecord.objects.all()
    serializer_class = AccountRecordSerializer

    @auth_required(role='user')
    def retrieve(self, request, pk=None):
        '''
        通过账户uuid查询指定账户记录
        '''
        # 过滤
        query_param = {
            'modify_balance__gte': request.GET.get('modify_balance__gte', None),
            'modify_balance__lte': request.GET.get('modify_balance__lte', None),
            'modify_source_uuid': request.GET.get('modify_source_uuid', None),
            'modify_source_type': request.GET.get('modify_source_type', None),
            'payment_account_uuid': pk
        }
        try:
            records = AccountRecord.objects.filter(**get_kwargs(query_param))
            count = records.count()
        except ValueError:
            log.error('[account] get account info error, payment_account_uuid: %s', pk)
            return Response({
                'detail': '参数错误',
                'error_code': '1400'
            }, status=status.HTTP_400_BAD_REQUEST)
        # 排序分页
        desc, limit, offset = get_query_paganaiton(request)
        queryset = records.order_by(desc + 'create_time')[offset:offset+limit]
        serializer = AccountRecordSerializer(queryset, many=True)
        return Response({'count':count,'content':serializer.data})


class RecordUserViewSet(viewsets.GenericViewSet):
    queryset = AccountRecord.objects.all()
    serializer_class = AccountRecordSerializer

    @auth_required(role='user')
    def list(self, request):
        '''
        # 通过user_uuid查询指定账户记录
        '''
        # 由用户ID反查账户ID
        accountset = PaymentAccount.objects.all()
        pk = request.GET.get('user_uuid')
        try:
            paymentAccount = get_object_or_404(accountset, user_uuid=pk)
            serializer, count = query_params_handler(request, pk=paymentAccount.payment_account_uuid)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '1400'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'count':count,'content':serializer.data})


def query_params_handler(request, pk=None):
    '''
    # 根据查询参数,进行排序分页
    '''
    order_by = request.GET.get('order_by', MODULE_PAYMENT_ACCOUNT['ORDER_BY'])
    desc, limit, offset = get_query_paganaiton(request)
    records = AccountRecord.objects.filter(payment_account_uuid=pk)
    count = records.count()
    queryset = records.order_by(desc + order_by)[offset:offset+limit]
    serializer = AccountRecordSerializer(queryset, context={'request': request}, many=True)
    return serializer, count
