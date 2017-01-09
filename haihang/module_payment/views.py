# -*- coding:utf-8 -*-

import logging
from django.shortcuts import get_object_or_404, get_list_or_404
# from django.db.transaction import TransactionManagementError
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from Payment.util import get_query_paganaiton, get_kwargs, get_config_value
from Payment.initConf import MODULE_PAYMENT
from module_payment.serializers import PaymentSerializer, PaymentRecordSerializer
from module_payment.serializers import PaymentCreateSerializer, PaymentRefundSerializer
from module_payment.models import Payment, PaymentRecord, PaymentRefund
from module_coupon.interface import binding_coupon, check_coupon
from module_payment_account.interface import get_account_by_user_uuid
from module_payment_account.models import PaymentAccount
from alipay.alipayCore import refund_fastpay_by_platform_pwd, create_direct_pay_by_alipay, notify_verify
from paypal.paypalCore import execute_payment, sale_refund

from interface import payment_charge_success, payment_refund_success, gen_no, get_real_price, pay_payment
from Payment.disable import CsrfExemptSessionAuthentication, auth_required

log = logging.getLogger('payment')

# Create your views here.
class PaymentViewSet(viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @auth_required(role='admin')
    def list(self, request):
        """
        支付单列表
        """
        # 过滤
        query_param = {
            'payment_uuid': request.GET.get('payment_uuid', None),
            'user_uuid': request.GET.get('user_uuid', None),
            'payment_no': request.GET.get('payment_no', None),
            'paid_method': request.GET.get('paid_method', None),
            'paid_status': request.GET.get('paid_status', None),
        }
        try:
            records = Payment.objects.filter(**get_kwargs(query_param))
            count = records.count()
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '3400'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 排序分页
        desc, limit, offset = get_query_paganaiton(request)
        queryset = records.order_by(desc + 'create_time')[offset:offset+limit]
        serializer = PaymentSerializer(queryset, many=True)
        return Response({'count':count,'content':serializer.data})

    @auth_required(role='user')
    def create(self, request):
        """
        创建订单接口
        {
            "user_uuid": "envid",
            "coupon_code": "string",
            "payment_price": "int",
            "paid_method":"alipay",
        }
        """

        # 获取用户账户信息
        try:
            user_uuid = request.data.get('user_uuid')
            payment_price = int(request.data.get('payment_price'))
            coupon_code = request.data.get('coupon_code', None)
            paid_method = request.data.get('paid_method')
            if payment_price > 9999999:
                return Response({
                    'detail': '充值金额过大',
                    'error_code': '2400'
                }, status=status.HTTP_400_BAD_REQUEST) 
            paymentAccount = get_account_by_user_uuid(user_uuid=user_uuid)
            log.info('[payment] user_uuid %s attemp to create payment by %s with coupon %s', 
                user_uuid, paid_method, coupon_code)
            if not paymentAccount:
                return Response({
                    'detail': 'user_uuid非法',
                    'error_code': '2400'
                }, status=status.HTTP_400_BAD_REQUEST)  
        except PaymentAccount.DoesNotExist:
            return Response({
                'detail': u'账户不存在',
                'error_code': '3404'
            },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            log.error(e)
            return Response({
                'detail': '参数错误',
                'error_code': '3400'
            }, status=status.HTTP_400_BAD_REQUEST)

        if coupon_code:
            coupon_user, coupon = binding_coupon(coupon_code, 
                                                paymentAccount.payment_account_uuid, 
                                                paymentAccount.user_uuid)
            real_price, payment_price = get_real_price(payment_price, coupon)
            if real_price is None:
                return Response({
                    'detail': '优惠码检测失败',
                    'error_code': '3410'
                }, status=status.HTTP_400_BAD_REQUEST)

            if not check_coupon(coupon):
                return Response({
                    'detail':u'优惠码不在有效期内',
                    'error_code': '3406'
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
            if paid_method in ('alipay', 'paypal') and coupon.coupon_type in ('discount', 'reduce') or \
                paid_method == 'coupon' and coupon.coupon_type == 'recharge':
                coupon_user.using_count_left = coupon_user.using_count_left - 1
                coupon_user.save()
                log.info('[payment] user_uuid %s use coupon_code %s', coupon_user.user_uuid, coupon_user.coupon_code)
            else:
                log.error('[payment] paid_method does not match coupon')
                return Response({
                    'detail': '支付方式与优惠码不匹配',
                    'error_code': '3410'
                }, status=status.HTTP_400_BAD_REQUEST)
            payment = Payment(
                user_uuid=paymentAccount.user_uuid,
                payment_account_uuid=paymentAccount.payment_account_uuid,
                payment_price = payment_price,
                real_price=real_price, 
                coupon_uuid=coupon.coupon_uuid,
                coupon_code=coupon.coupon_code)
        else:
            # 未使用优惠码
            real_price = payment_price
            payment = Payment(
                user_uuid=paymentAccount.user_uuid,
                payment_account_uuid=paymentAccount.payment_account_uuid,
                payment_price = payment_price,
                real_price=real_price)

        payment.paid_method = paid_method
        err, value = pay_payment(payment)
        if not err:
            return Response(value, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'url': value})

    @auth_required(role='admin')
    def retrieve(self, request, pk=None):
        """
        获取订单详情
        """
        queryset = Payment.objects.all()
        try:
            payment = get_object_or_404(queryset, pk=pk)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '3400'
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = PaymentSerializer(payment, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['get'])
    @auth_required(role='admin')
    def record(self, request, pk=None):
        """
        获取订单处理记录详情
        """
        queryset = PaymentRecord.objects.all()
        try:
            record = get_list_or_404(queryset, payment_uuid=pk)
            serializer = PaymentRecordSerializer(record, context={'request': request}, many=True)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '3400'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)


    @detail_route(methods=['post'])
    def refund(self, request, pk=None):
        """
        支付单退款接口
        {
            "approval_result": "agree or disagree"
        }
        """
        try:
            queryset = Payment.objects.all()
            payment = get_object_or_404(queryset, pk=pk)
            refundset = PaymentRefund.objects.filter(refund_status='waiting')
            payment_refund = get_object_or_404(refundset, payment_uuid=pk)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '3400'
            }, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('approval_result') != 'agree':
            payment_refund.refund_status = 'refuse'
            payment_refund.save()
            return Response({'detail': u'refused refund'})
        if payment.paid_method == 'alipay':
            # 退款请求时间
            refund_date = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            # 批次号
            batch_no = gen_no('batch_no')
            # 注意, 交易号并非订单号
            trade_no = payment.sale_id
            total_fee = str(payment.real_price / 100.0)
            refund_reason = payment_refund.refund_reason or MODULE_PAYMENT['REFUND_REASON']
            # url给到后台, 并非前端
            url = refund_fastpay_by_platform_pwd(refund_date, batch_no, trade_no, total_fee, refund_reason)
            result = {'detail': u'gen url success', 'url': url}
        else:
            # paypal不用等待回调
            refund = sale_refund(payment.sale_id) 
            if refund.success():
                # 退款
                payment_refund_success(payment, request.data)
                payment_refund.refund_status = 'success'
                payment_refund.save()
                result = {'detail': u'refund success'}
            else:
                log.error('[payment] refund %s error', payment_refund.payment_refund_uuid)
                result = {'detail': u'refund fail'}
        return Response(result)

    @detail_route(methods=['post'])
    def pre_refund(self, request, pk=None):
        """
        支付单退款申请接口
        {
            "refund_reason":"想退就退"
        }
        """
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({
                'detail': 'Not found',
                'error_code': '未找到该支付单'
            }, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '3400'
            }, status=status.HTTP_400_BAD_REQUEST)


        if payment.paid_status != 'success':
            return Response({
                'detail': u'订单未成功支付',
                'error_code': '3406'
            },status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            payment_refund = PaymentRefund.objects.get(payment_uuid=payment)
            return Response({
                'detail': u'The payment slip has been requested for a refund',
                'error_code': '订单已申请付款'
            },status=status.HTTP_409_CONFLICT)
        except PaymentRefund.DoesNotExist:
            serializer = PaymentRefundSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(payment_uuid=payment)
            else:
                return Response({
                    'detail': '参数错误',
                    'error_code': '3400'
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data)

    @list_route(methods=['get'])
    def alipay_return_url(self, request):
        """
        支付宝同步回调接口
        """
        # if notify_verify(request.data) is False:
        #     print '签名验证失败'
        #     return HttpResponse('fail')
    	#     print request.query_params
        #  return HttpResponse('success')
        #    完成的url
        return HttpResponseRedirect(get_config_value('redirect_url') + '/wallet')

    @list_route(methods=['post'])
    def alipay_notify_url(self, request):
        """
        支付宝异步回调接口
        """
        payment_no = request.data.get('out_trade_no')
        log.info('[payment] received payment_no: %s', payment_no)
        if notify_verify(request.POST) is False:
            log.warning('[payment] notify_verify error')
            return HttpResponse('fail')
        try:
            payment = Payment.objects.get(payment_no=payment_no)
            # 交易失败直接返回
            if request.data.get('trade_status') not in ('TRADE_SUCCESS', 'TRADE_FINISHED') and \
                payment.paid_status == 'waiting':
                payment.paid_status = 'failed'
                payment.save()
                return HttpResponse('success')
            payment_charge_success(payment, request.data)
        except Payment.DoesNotExist:
            log.error('[payment] no such payment_no %s', payment_no)
        return HttpResponse('success')

    @list_route(methods=['post'])
    def alipay_refund_url(self, request):
        """
        支付宝退款回调接口
        """
        payment_no = request.data.get('out_trade_no')
        log.info('[payment] received refund, payment_no: %s', payment_no)
        if notify_verify(request.POST) is False:
            return HttpResponse('fail')
        try:
            sale_id = request.data.get('result_details').split('^')[0]
            payment = Payment.objects.get(sale_id=sale_id)
            payment_refund = PaymentRefund.objects.get(payment_uuid=payment.payment_uuid, refund_status='waiting')
            if request.data.get('success_num') != '1':
                # 退款失败
                return HttpResponse('success')
            payment_refund_success(payment, request.data)
            payment_refund.refund_status = 'success'
            payment_refund.save()
        except Payment.DoesNotExist:
            log.error('[payment] no such payment_no %s', payment_no)
        except PaymentRefund.DoesNotExist:
            log.error('[payment] no such refund %s', payment.payment_uuid)
        return HttpResponse('success')
    


    @list_route(methods=['get'])
    def paypal_return_url(self, request):
        """
        paypal 余额支付回调接口
        """
        payment_no = request.query_params.get('paymentId')
        log.info('[payment] received paypal payment_no: %s', payment_no)
        payer_id = request.query_params.get('PayerID')
        try:
            payment = Payment.objects.get(payment_no=payment_no)
        except Payment.DoesNotExist:
            log.error('[payment] no such payment %s', )
            return Response({
                'error': u'未发现订单',
                'error_code': '3404'
            }, status=status.HTTP_404_NOT_FOUND)

        paypal_payment = execute_payment(payment_no, payer_id)
        if paypal_payment is None and payment.paid_status == 'waiting':
            # 交易失败 
            payment.paid_status = 'failed'
            payment.save()
            return Response({'error': u'charge fail'})

        for transaction in paypal_payment.transactions:
            for related_resource in transaction.related_resources:
                sale_id = related_resource.sale.id
                payment.sale_id = sale_id
                sale_state = related_resource.sale.state
        # 充值
        payment_charge_success(payment, request.query_params)
        # return Response({'success': u'charge success'})
        return HttpResponseRedirect(get_config_value('redirect_url') + '/wallet')




class PaymentUserViewSet(viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @auth_required(role='user')
    def list(self, request):
        """
        获取指定用户订单列表(充值记录)
        """
        pk = request.GET.get('user_uuid')
        try:
            records = Payment.objects.filter(user_uuid=pk, paid_status='success')
            count = records.count()
            # 排序分页
            desc, limit, offset = get_query_paganaiton(request)
            queryset = records.order_by(desc + 'create_time')[offset:offset+limit]
            serializer = PaymentSerializer(queryset, many=True)
            return Response({'count':count,'content':serializer.data})
        except ValueError:
            return Response({
                'detail': '参数错误',
                'error_code': '3400'
            }, status=status.HTTP_400_BAD_REQUEST)

