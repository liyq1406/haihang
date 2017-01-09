# -*- coding:utf-8 -*-
from configure.models import Configure
from configure.serializers import ConfigureSerializer
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import list_route
from rest_framework.response import Response
import time
# Create your views here.

class ConfigureViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset = Configure.objects.all()
    serializer_class = ConfigureSerializer

    def list(self, request):
        '''
        # 读取数据库中保存的全部配置
        '''       
        arr = {}
        queryset = Configure.objects.all()
        for item in queryset:
            if item.code in ['paypal_client_id','paypal_client_secret','paypal_mode','alipay_partner','alipay_key','alipay_seller_email']:
                continue
            else:
                arr[item.code] = item.value
    
        return Response(arr)
    
    @list_route(methods=['post'])
    def save(self, request):
        '''
        # 保存配置
        '''
        arr = []
        queryset = Configure.objects.all()
        for item in queryset:
            v = str(request.data.get(item.code)) if item.code in request.data else item.value
            if v != item.value:
                rlt = Configure.objects.filter(code=item.code).update(value = v)
                if rlt:
                    arr.append(item.code)
            
        return Response(arr, status=status.HTTP_201_CREATED)
    
    @list_route(methods=['get','post'])
    def ready(self, request):
        return Response(time.time(), status=status.HTTP_200_OK)
        