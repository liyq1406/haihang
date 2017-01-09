# -*- coding:utf-8 -*-

import logging
from Payment.util import get_query_paganaiton, get_kwargs
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import detail_route
from .serializers import ReconciliationDealSerializer, ReconciliationSerializer, ReconciliationGetSerializer
from .models import Reconciliation
from Payment.disable import CsrfExemptSessionAuthentication, auth_required

log = logging.getLogger('module_reconciliation')

class ReconciliationViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Reconciliation.objects.all()
    serializer_class = ReconciliationSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @auth_required(role='admin')
    def list(self, request):
        """
        对账异常列表
        """
        # 过滤
        query_param = {
            'payment_no': request.GET.get('payment_no', None),
            'error_type': request.GET.get('error_type', None),
            'deal_status': request.GET.get('deal_status', None),
        }
        try:
            records = Reconciliation.objects.filter(**get_kwargs(query_param))
            count = records.count()
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '4400'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 排序分页
        desc, limit, offset = get_query_paganaiton(request)
        queryset = records.order_by(desc + 'create_time')[offset:offset+limit]
        serializer = ReconciliationSerializer(queryset, many=True)
        return Response({'count':count,'content':serializer.data})

    @auth_required(role='admin')
    def retrieve(self, request, pk=None):
        """
        查询指定对账异常记录
        """
        queryset = Reconciliation.objects.all()
        try:
            reconciliation = get_object_or_404(queryset, pk=pk)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '4400'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer= ReconciliationGetSerializer(reconciliation, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    @auth_required(role='admin')
    def deal(self, request, pk=None):
        """
        对账异常处理
        """
        queryset = Reconciliation.objects.all()
        try:
            reconciliation = get_object_or_404(queryset, pk=pk)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '4400'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = ReconciliationDealSerializer(reconciliation, data=request.data)
        if not request.data.get('deal_result'):
            return Response({
                'detail': '参数错误',
                'error_code': '4400'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('deal_status'):
            return Response({
                'detail': '参数错误',
                'error_code': '4400'
            }, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save(
                deal_result=request.data.get('deal_result'),
                deal_status=request.data.get('deal_status'))
            return Response(serializer.data)
        else:
            return Response({
                'detail': '参数错误',
                'error_code': '4400'
            }, status=status.HTTP_400_BAD_REQUEST)
