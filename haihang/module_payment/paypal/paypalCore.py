# -*- coding:utf-8 -*-

import paypalrestsdk, logging
from paypalrestsdk import Sale, ResourceNotFound, Payment
from paypalConfig import Settings

settings = Settings()
log = logging.getLogger('payment')

paypalrestsdk.configure({
    "mode": settings.MODE, 
    "client_id": settings.CLIENT_ID,
    "client_secret": settings.CLIENT_SECRET})

"""
def create_webhook():
    webhook = Webhook({
        "url": settings.WEBHOOK_URL,
        "event_types": [{
            "name": "PAYMENT.SALE.COMPLETED"
        }, {
            "name": "PAYMENT.SALE.DENIED"
        }]
    })
    if webhook.create():
        print("Webhook[%s] created successfully" % (webhook.id))
        return True
    else:
        print(webhook.error)
        return False
"""
# create_webhook()

def create_direct_pay_by_paypal(payment_method, name, description, total_fee, **kwargs):
    """
    paypal及时到账接口
    paid_method: 支付方式 paypal_balance, visa
    intent: payment类型 sale, authorize, order
    total_fee: 价格
    name: 商品名称
    description: 商品描述
    **kwargs: 信用卡方式信用卡信息 number, expire_month, expire_year, cvv2
    """
    if payment_method == 'paypal_balance':
        # paypal余额会确认订单, 生成重定向连接
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": settings.RETURN_URL,
                "cancel_url": settings.CANCEL_URL},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": name,
                        "price": total_fee,
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": total_fee,
                    "currency": "USD"},
                "description": description}]})
    else:
        # 信用卡将不会有确认动作, 将直接执行扣款
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [{
                    "credit_card": {
                        "type": "visa",
                        "number": kwargs['number'],
                        "expire_month": kwargs['expire_month'],
                        "expire_year": kwargs['expire_year']}}]},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": name,
                        "price": total_fee,
                        "currency": "USD",
                        "quantity": 1}]},
                "amount": {
                    "total": total_fee,
                    "currency": "USD"},
                "description": description}]})
    # Create Payment and return status
    if payment.create():
        log.info('[payment] paypal payment %s create success', payment.id)
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                return redirect_url, payment.id
        return payment, None
    else:
        log.error('[payment] paypal payment create fail, %s', payment.error)
        return None, None

def execute_payment(payment_id, payer_id):
    """
    paypal执行付款
    payment_id: 账单ID
    payer_id: 客户ID
    """
    payment = Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}): 
        log.info('[payment] paypal payment %s execute success', payment.id)
        return payment
    else:
        log.error('[payment] paypal payment execute fail, %s', payment.error)
        return None

def sale_refund(sale_id):
    """
    paypal 退款
    sale_id: sale_id
    """
    try:
        sale = Sale.find(sale_id)
        refund = sale.refund({})
        log.info('[payment] paypal sale_id: %s refund success', sale_id)
        return refund
    except ResourceNotFound as error:
        log.info('[payment] paypal sale_id: %s refund fail', sale_id)
        return None

def find_paypal_payment(payment_id):
    try:
        payment = Payment.find(payment_id)
    except ResourceNotFound as error:
        payment = None
    return payment

def paypal_payment_history(**kwargs):
    query_param = {
        'count': 100,
        'sort_by': 'create_time',
        'sort_order': 'desc',
        'start_time': kwargs['start_time'],
        'end_time': kwargs['end_time']
    }
    if kwargs.get('start_id'):
        query_param['start_id'] = kwargs['start_id']
    payment_history = Payment.all(query_param)
    return payment_history