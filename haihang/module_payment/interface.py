# -*- coding:utf-8 -*-

import logging, json, random
from django.utils import timezone
from models import PaymentRecord
from module_payment_account.interface import change_balance
from Payment.initConf import MODULE_PAYMENT
from module_coupon.interface import use_coupon
from alipay.alipayCore import create_direct_pay_by_alipay
from paypal.paypalCore import find_paypal_payment, create_direct_pay_by_paypal
from paypal.exchange_rate import CNY_USD

log = logging.getLogger('payment')

def payment_charge_success(payment, data, source='payment'):
    """
    充值成功处理方法
    """
    payment.paid_status = 'success'

    if payment.paid_method == 'alipay':
        payment.sale_id = data.get('trade_no')
    try:
        # 优惠码使用
        if payment.coupon_uuid or payment.coupon_code:
            use_result = use_coupon(
                            payment_account_uuid=payment.payment_account_uuid, 
                            user_uuid=payment.user_uuid, 
                            usage_source_type=source,
                            usage_source_uuid=payment.payment_uuid,
                            coupon_code=payment.coupon_code)
            if not use_result:
                return False
        # 用户账户充值
        charge_result = change_balance(
                            payment.user_uuid,
                            source,
                            payment.payment_price,
                            payment.payment_uuid)
        if not charge_result:
            return False
        # 支付单处理记录
        payment_record = PaymentRecord(
                            payment_uuid=payment,
                            paid_method=payment.paid_method,
                            pay_response_data=json.dumps(data))
        payment.save()
        payment_record.save()
        log.info('[payment] payment %s charge success', payment.payment_uuid)
        return True
    except Exception as e:
        log.error(e)
        log.error('[payment] payment %s charge fail', payment.payment_uuid)
        return False

def payment_refund_success(payment, data):
    payment.paid_status = 'refunded'
    # 用户账户减扣
    try:
        charge_result = change_balance(
                            payment.user_uuid,
                            'refund',
                            -payment.payment_price,
                            payment.payment_uuid)
        if not charge_result:
            return False
        # 支付单处理记录
        payment_record = PaymentRecord(
                            payment_uuid=payment,
                            paid_method=payment.paid_method,
                            pay_response_data=json.dumps(data))
        payment.save()
        payment_record.save()
        log.info('[payment] payment %s refund success', payment.payment_uuid)
    except Exception as e:
        log.error(e)
        log.error('[payment] payment %s refund fail', payment.payment_uuid)

def gen_no(type='payment_no'):
    """
    生产订单号, 批次
    """
    if type == 'payment_no':
        return ''.join(ch for ch in str(unicode(timezone.now()))[2:25] if ch not in (" ","-",":",".")) \
                + ''.join([random.choice('123456789') for _ in range(8)])
    else:
        return timezone.now().strftime('%Y%m%d') + ''.join([random.choice('0123456789') for _ in range(4)])

def repay_payment(payment):
    subject = MODULE_PAYMENT['SUBJECT']
    body = MODULE_PAYMENT['BODY']
    try:
        if payment.payment_method == 'alipay':
            log.info('[payment] repay alipay payment %s', payment.payment_uuid)
            return create_direct_pay_by_alipay(payment.payment_no, subject, body, payment.real_price / 100.0)  
        elif payment.payment_method == 'paypal':
            log.info('[payment] repay paypal payment %s', payment.payment_uuid)
            paypal_payment = find_paypal_payment(payment.payment_no)
            if paypal_payment:
                for link in paypal_payment.links:
                    if link.method == "REDIRECT":
                        return str(link.href)
    except Exception as e:
        log.error(e)
    return False

def get_real_price(payment_price, coupon):
    if not coupon:
        log.info('[payment] not a valid coupon')
        return None, None
    elif coupon.coupon_type == 'discount':
        real_price = coupon.coupon_value * payment_price / 100.0
    elif coupon.coupon_type == 'reduce':
        real_price = 1 if coupon.coupon_value >= payment_price else (payment_price - coupon.coupon_value)
    elif coupon.coupon_type == 'recharge':
        real_price = 0
        payment_price = coupon.coupon_value
    else:
        log.error('[payment] no such coupon type')
        return None, None
    return real_price, payment_price

def pay_payment(payment):
    # 实际支付价格为0, 支付方式为优惠码充值支付
    if (payment.real_price == 0 and payment.paid_method != 'coupon') or \
        (payment.real_price != 0 and payment.paid_method == 'coupon'):
        log.error('[payment] paid_method does not match coupon')
        return False, {'detail':u'支付方式与优惠码不匹配','error_code': '3400'}

    subject = MODULE_PAYMENT['SUBJECT']
    body = MODULE_PAYMENT['BODY']
    if payment.paid_method == 'alipay':
        out_trade_no = gen_no('payment_no')
        payment.payment_no = out_trade_no
        total_fee = payment.real_price / 100.0 # 系统单位分 ===> 支付宝单位圆
        url = create_direct_pay_by_alipay(out_trade_no, subject, body, total_fee)  
        log.info('[payment] gen url %s for payment_no', url, out_trade_no)
    elif payment.paid_method == 'paypal':
        capital_source = 'paypal_balance'
        total_fee, rate = CNY_USD(payment.real_price / 100.0)
        log.info('[payment] %s rate is %f', payment.payment_uuid, rate)
        payment.real_price = total_fee * 100
        url, payment_no = create_direct_pay_by_paypal(capital_source, subject, body, total_fee)
        if payment_no is None:
            return False, {'detail': u'生成paypal订单失败','error_code': '3500'}
        log.info('[payment] gen url %s for payment_no', url, payment_no)
        payment.payment_no = payment_no
    elif payment.paid_method == 'coupon':
        payment.payment_no = gen_no('payment_no')
        if payment_charge_success(payment, {}):
            return True, '####'
        else:
            return False, {'detail':u'优惠码充值失败','error_code': '3500'}
    else:
        return False, {'detail': u'无效的支付方式','error_code': '3400'}
    payment.paid_status = 'waiting'
    payment.save()
    return True, url
