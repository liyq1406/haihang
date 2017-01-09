# -*- coding:utf-8 -*-

from Payment.disable import CsrfExemptSessionAuthentication, auth_required
from Payment.initConf import MODULE_COUPON
from Payment.util import get_kwargs, get_query_paganaiton
from django.shortcuts import get_object_or_404
from django.utils import timezone
from module_coupon.interface import binding_coupon
from module_coupon.models import Coupon, CouponUsage, CouponUser
from module_coupon.serializers import CouponCreateSerializer, CouponSerialzer, \
    CouponUserSerialzer, CouponUsageSerialzer
from module_payment_account.interface import get_account_by_user_uuid
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
import logging
import random
import string
import time

log = logging.getLogger('payment')


class CouponViewSet(viewsets.GenericViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponCreateSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @auth_required(role='admin')
    @list_route(methods=['GET'])
    def list_all(self, request):
        """
        优惠码列表
        """
        # 过滤
        query_param = {
            'coupon_code': request.GET.get('coupon_code', None),
            'coupon_uuid': request.GET.get('coupon_uuid', None),
            'coupon_type': request.GET.get('coupon_type', None),
            'coupon_value__gte': request.GET.get('coupon_value__gte', None),
            'coupon_value__lte': request.GET.get('coupon_value__lte', None),
            'valid_datetime_start__lte': request.GET.get('valid_datetime_start__lte', None),
            'valid_datetime_end__gte': request.GET.get('valid_datetime_end__gte', None),
        }
        try:
            records = Coupon.objects.filter(**get_kwargs(query_param))
            count = records.count()
        except ValueError:
            log.error('[coupon] list coupon error queryset: %s', str(queryset))
            return Response({
                'detail': '参数错误',
                'error_code': '2400'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 排序分页
        desc, limit, offset = get_query_paganaiton(request)
        queryset = records.order_by(desc + 'create_time')[offset:offset+limit]
        serializer = CouponSerialzer(queryset, many=True)
        return Response({'count':count,'content':serializer.data})

    @auth_required(role='user')
    def list(self, request):
        """
        未失效优惠码列表
        """
        try:
            now = timezone.make_aware(timezone.datetime.now())
            # 有剩余可用人数,且结束时间小于当前时间视为有效优惠码
            queryset = Coupon.objects.filter(using_user_left__gt=0, valid_datetime_end__gt=now)
            count = queryset.count()
            serializer = CouponSerialzer(queryset, many=True)
            return Response({'count':count,'content':serializer.data})
        except Exception as e:
            log.error('[coupon] e: %s', e)
            return Response({'detail': '内部错误','error_code':'2500'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @auth_required(role='superadmin')
    def create(self, request):
        """
        批量创建优惠码
        {
            "valid_datetime_start": "2016-10-31 07:45:34",
            "create_count": 5,
            "coupon_type": "discount",
            "coupon_using_count": 10,
            "coupon_value": 500,
            "valid_datetime_end": "2016-12-25 07:45:34",
            "coupon_using_user": 10
        }
        """
        serializer = CouponCreateSerializer(data=request.data)
        if serializer.is_valid():
            create_count = int(request.data.get('create_count'))
            # 缓存查询集
            queryset = Coupon.objects.all()
            chars = string.uppercase + string.digits
            # 优惠码临时缓存
            code_list_temp = []
            code_list_valid = []
            # 批量生成优惠码
            while len(code_list_valid) < create_count:
                s = [random.choice(chars) for _ in range(MODULE_COUPON['COUPON_CODE_LEN'])]
                code = ''.join(s)
                if code not in code_list_temp and queryset.filter(coupon_code=code).count()==0:
                    code_list_valid.append(code)
                code_list_temp.append(code)
            
            # 保存优惠码到coupon_当前时间.txt文件以及数据库中
            
            coupon_path = ''.join(['data/coupon/', str(time.time()).replace('.','_'), '.txt'])
            coupon_type = request.data.get('coupon_type')
            coupon_using_count = request.data.get('coupon_using_count')
            coupon_using_user = request.data.get('coupon_using_user')
            get_start = request.data.get('valid_datetime_start')
            get_end = request.data.get('valid_datetime_end')
            valid_datetime_start =  timezone.datetime.strptime(get_start, '%Y-%m-%dT%H:%M:%S.%fZ')
            valid_datetime_start = timezone.make_aware(valid_datetime_start)
            valid_datetime_end =  timezone.datetime.strptime(get_end, '%Y-%m-%dT%H:%M:%S.%fZ')
            valid_datetime_end = timezone.make_aware(valid_datetime_end)
            coupon_value = request.data.get('coupon_value')
            if coupon_type == 'discount' and coupon_value >= 100:
                log.error('[coupon] discount coupon value greater than 100')
                return Response({
                    'detail':u'参数错误',
                    'error_code': '2400'
                }, status.HTTP_400_BAD_REQUEST)
            try:
                f = open(coupon_path, 'wb')
                for code in code_list_valid:
                    f.write(code + '\n')
                    coupon = Coupon(coupon_code=code, coupon_type=coupon_type, 
                                    coupon_using_count=coupon_using_count,
                                    coupon_using_user=coupon_using_user,
                                    using_user_left=coupon_using_user,
                                    valid_datetime_start=valid_datetime_start,
                                    valid_datetime_end=valid_datetime_end,
                                    coupon_value=coupon_value)
                    coupon.save()
                f.close()
                serializer.save(coupon_codes=code_list_valid, coupon_path=coupon_path.replace('data/coupon/', ''))
                log.info('[coupon] create %d coupon codes at %s.',create_count, coupon_path)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IOError:
                log.error('[coupon] write file %s fail', coupon_path)
                return Response({
                    'detail':u'优惠码写入失败',
                    'error_code': '2500'
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                log.error(e)
                log.error('[coupon] create coupon error ')
                return Response({
                    'detail':u'创建优惠码失败',
                    'error_code': '2501'
                }, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({
                'detail': '参数错误',
                'error_code': '2400'
            },status=status.HTTP_400_BAD_REQUEST)

    @auth_required(role='user')
    def retrieve(self, request, pk=None):
        """
        获取优惠码详情, 可以输入优惠码uuid或优惠码code
        """
        queryset = Coupon.objects.all()
        try:
            if len(pk)==MODULE_COUPON['COUPON_CODE_LEN']:
                coupon = get_object_or_404(queryset, coupon_code=pk)
            else:
                coupon = get_object_or_404(queryset, pk=pk)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '2400'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = CouponSerialzer(coupon, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['post'])
    @auth_required(role='user')
    def binding(self, request, pk=None):
        """
        # 用户与优惠码绑定
        """
        try:
            user_uuid = request.data.get('user_uuid')
            paymentAccount = get_account_by_user_uuid(user_uuid=user_uuid)
            if not paymentAccount:
                return Response({
                    'detail': 'user_uuid非法',
                    'error_code': '2400'
                }, status=status.HTTP_400_BAD_REQUEST)   
            coupon_user, coupon = binding_coupon(pk, paymentAccount.payment_account_uuid, user_uuid)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '2400'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not coupon:
            return Response({
                'detail':'无效的优惠码',
                'error_code': '2401'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CouponUserSerialzer(coupon_user)
            return Response(serializer.data)

    @list_route(methods=['GET'])
    @auth_required(role='user')
    def usage(self, request):
        """
        # 查询指定条件下优惠码使用记录
        """
        # 过滤
        query_param = {
            'coupon_code': request.GET.get('coupon_code', None),
            'user_uuid': request.GET.get('user_uuid', None),
            'coupon_usage_uuid': request.GET.get('coupon_usage_uuid', None),
            'usage_source_type': request.GET.get('usage_source_type', None),
            'usage_source_uuid': request.GET.get('usage_source_uuid', None),
        }
        try:
            records = CouponUsage.objects.filter(**get_kwargs(query_param))
            count = records.count()
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '2400'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 排序分页
        desc, limit, offset = get_query_paganaiton(request)
        queryset = records.order_by(desc + 'use_time')[offset:offset+limit]
        serializer = CouponUsageSerialzer(queryset, many=True)
        return Response({'count':count,'content':serializer.data})

    @list_route(methods=['GET'])
    @auth_required(role='user')
    def bindings(self, request):
        """
        # 查询指定用户所绑定的优惠码
        """
        user_uuid = request.GET.get('user_uuid', None)
        try:
            records = CouponUser.objects.filter(user_uuid=user_uuid)
            count = records.count()
            serializer = CouponUserSerialzer(records, many=True)
            return Response({'count':count,'content':serializer.data})
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '2400'
            }, status=status.HTTP_400_BAD_REQUEST)
