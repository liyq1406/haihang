# -*- coding:utf-8 -*-
 
from __future__ import absolute_import, unicode_literals
from .models import Reconciliation
from Payment.settings import BASE_DIR
from Payment.util import get_kwargs
from module_payment.alipay.alipayCore import alipay_payment_history, xml_verify
from module_payment.models import Payment
from module_payment.paypal.paypalCore import paypal_payment_history
from urllib import urlopen
import csv
import datetime
import logging
import os
import xml.etree.cElementTree as ET
# from celery.task.schedules import crontab  
# from celery.decorators import periodic_task

log = logging.getLogger('payment')

def check_paypal():
    """
    定时任务, 每天凌晨2点处理paypal对账单
    start_time='2016-11-05T00:00:00Z'
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%dT00:00:00Z')
    today_str = today.strftime('%Y-%m-%dT00:00:00Z')

    try:
        file_path = get_work_path('data', 'csv', yesterday.strftime('%Y-%m-%d') + '_paypal.csv')
        csvfile = file(file_path, 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(['A_payment_uuid', 'A_user_uuid', 'A_payment_account_uuid', 'A_payment_no', \
                        'A_payment_price', 'A_paid_method', 'A_real_price', 'A_sale_id', \
                        'A_coupon_uuid', 'A_coupon_code', 'A_paid_status', 'A_create_time', \
                        'B_id', 'B_state', 'B_create_time', 'B_transaction_fee', 'B_total', \
                        'B_email', 'B_payer_id', 'B_first_name', 'B_last_name', 'B_payment_method'])
        ph = paypal_payment_history(
            start_time=yesterday_str, 
            end_time=today_str)
        if ph.count == 0:
            return True
        check_paypal_detail(ph, writer)
        while ph.next_id:
            start_id = ph.next_id
            ph = paypal_payment_history(
                start_time=yesterday_str, 
                end_time=today_str,
                start_id=start_id)
            check_paypal_detail(ph, writer)
    except Exception as e:
        log.error(e)
    csvfile.close()
    

def get_work_path(*folders):
    return os.path.join(BASE_DIR, *folders)
    


def check_alipay():
    """
    定时任务, 每天凌晨2点处理alipay对账单
    """
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d 00:00:00')
    today_str = today.strftime('%Y-%m-%d 00:00:00')
    try:
        file_path = get_work_path('data', 'csv', yesterday.strftime('%Y-%m-%d') + '_alipay.csv')
        csvfile = file(file_path, 'wb')
        writer = csv.writer(csvfile)
        writer.writerow(['A_payment_uuid', 'A_user_uuid', 'A_payment_account_uuid', 'A_payment_no', \
                        'A_payment_price', 'A_paid_method', 'A_real_price', 'A_sale_id', \
                        'A_coupon_uuid', 'A_coupon_code', 'A_paid_status', 'A_create_time', \
                        'B_merchant_out_order_no', 'B_total_fee', 'B_trade_refund_amount', \
                        'B_service_fee', 'B_trade_no', 'B_trans_date', 'B_buyer_account'])

        page_no = 1
        has_next_page = check_alipay_detail(page_no, yesterday_str, today_str, '100', writer)
        while has_next_page == 'T':
            page_no += 1
            has_next_page = check_alipay_detail(page_no, yesterday_str, today_str, '100', writer)
    except Exception as e:
        log.error(e)
    csvfile.close()

def check_alipay_detail(page_no, yesterday_str, today_str, page_size, writer):
    try:
        url = alipay_payment_history(page_no, yesterday_str, today_str, page_size)
        log.info('[reconciliation] query %s success', url)
        fp = urlopen(url)
        if fp.getcode() != 200:
            log.error('[reconciliation] query %s error', url)
        else:
            tree = ET.parse(fp)
            root = tree.getroot() 
            is_success = root.findtext('is_success')
            sign = root.findtext('sign')
            result = root.find('response/account_page_query_result')
            has_next_page = result.findtext('has_next_page')
            page_no = result.findtext('page_no')
            page_size = result.findtext('page_size')
            account_log_list = result.find('account_log_list')
            try:
                log_str = ET.tostring(account_log_list, encoding='utf-8').replace(" ", "")
            except Exception, e: 
                log_str = ET.tostring(account_log_list, encoding='utf-8')

            params = {
                'account_log_list': log_str,
                'has_next_page': has_next_page,
                'page_no': page_no,
                'page_size': page_size,
                'sign': sign
            }
            if xml_verify(params):
                for item in account_log_list.iterfind('AccountQueryAccountLogVO'):
                    merchant_out_order_no = item.findtext('merchant_out_order_no')
                    total_fee = item.findtext('total_fee')
                    trade_refund_amount = item.findtext('trade_refund_amount')
                    service_fee = item.findtext('service_fee')
                    trade_no = item.findtext('trade_no')
                    trans_date = item.findtext('trans_date')
                    buyer_account = item.findtext('buyer_account').encode('utf-8')
                    record = {
                        'payment_no': merchant_out_order_no,
                        'payment_record': u' ',
                        'third_record': ET.tostring(item, encoding='utf-8')
                    }
                    csvrow = []
                    try:
                        payment_record = Payment.objects.get(payment_no=merchant_out_order_no)
                        record['payment_record'] = payment_record.payment_uuid
                        if abs(payment_record.real_price - float(total_fee) * 100) > 0.01:
                            record['error_type'] = u'amount'
                            reconciliation_save(**get_kwargs(record))
                            log.error('[reconciliation] alipay amount valid fail %s', merchant_out_order_no)
                        if trade_refund_amount == '0.00' and payment_record.paid_status != 'success':
                            record['error_type'] = u'status'
                            reconciliation_save(**get_kwargs(record))
                            log.error('[reconciliation] alipay status valid fail %s', merchant_out_order_no)
                        csvrow = get_payment_info(payment_record) + [merchant_out_order_no, total_fee, \
                            trade_refund_amount, service_fee, trade_no, trans_date, buyer_account]
                    except Payment.DoesNotExist:
                        record['error_type'] = u'miss'
                        reconciliation_save(**get_kwargs(record))
                        log.error('[reconciliation] alipay record miss %s', merchant_out_order_no)
                        csvrow = get_payment_info() + [merchant_out_order_no, total_fee, \
                            trade_refund_amount, service_fee, trade_no, trans_date, buyer_account]
                    except Payment.MultipleObjectsReturned:
                        record['error_type'] = u'multi'
                        reconciliation_save(**get_kwargs(record))
                        log.error('[reconciliation] alipay record multi %s', merchant_out_order_no)
                        csvrow = get_payment_info() + [merchant_out_order_no, total_fee, \
                            trade_refund_amount, service_fee, trade_no, trans_date, buyer_account]
                    log.info(csvrow)
                    writer.writerow(csvrow)
                    
            else:
                log.error('[reconciliation] verify error: %s', url)
        fp.close()
        return has_next_page
    except Exception, e: 
        log.error(e)
        return None

def check_paypal_detail(paypal_history, writer):
    for payment in paypal_history.payments:
        # 获取账单金额
        for transaction in payment.transactions:
            payment_amount = transaction.amount.total

        record = {
            'payment_no': payment.id,
            'payment_record': u' ',
            'third_record':str(payment)
        }
        csvrow = []
        try:
            payment_record = Payment.objects.get(payment_no=payment.id)
            record['payment_record'] = payment_record.payment_uuid
            if abs(payment_record.real_price - float(payment_amount) * 100) > 0.01:
                record['error_type'] = u'amount'
                reconciliation_save(**get_kwargs(record))
                log.error('[reconciliation] paypal amount valid fail %s', payment.id)
            if payment.state == 'approved' and payment_record.paid_status != 'success':
                record['error_type'] = u'status'
                reconciliation_save(**get_kwargs(record))
                log.error('[reconciliation] paypal status valid fail %s', payment.id)
            csvrow = get_payment_info(payment_record) + get_paypal_info(payment)
        except Payment.DoesNotExist:
            record['error_type'] = u'miss'
            reconciliation_save(**get_kwargs(record))
            log.error('[reconciliation] paypal record miss %s', payment.id)
            csvrow = get_payment_info() + get_paypal_info(payment)
        except Payment.MultipleObjectsReturned:
            record['error_type'] = u'multi'
            reconciliation_save(**get_kwargs(record))
            log.error('[reconciliation] paypal record multi %s', payment.id)
            csvrow = get_payment_info() + get_paypal_info(payment)
        log.info(csvrow)
        writer.writerow(csvrow)


def reconciliation_save(**kwargs):
    rec = Reconciliation(**kwargs)
    rec.save()

def get_payment_info(payment=None):
    if payment is None:
        return ['', '', '', '', '', '', '', '', '', '', '', '']
    return [payment.payment_uuid, payment.user_uuid, payment.payment_account_uuid, payment.payment_no, \
            payment.payment_price, payment.paid_method, payment.real_price, payment.sale_id, \
            payment.coupon_uuid, payment.coupon_code, payment.paid_status, payment.create_time]

def get_paypal_info(paypal):
    for transaction in paypal.transactions:
        total = transaction.amount.total
        for related_resource in transaction.related_resources:
            transaction_fee = related_resource.sale.transaction_fee.value
    payer_info = paypal.payer.payer_info
    return [paypal.id, paypal.state, paypal.create_time, transaction_fee, total, payer_info.email, \
        payer_info.payer_id, payer_info.first_name.encode('utf-8'), payer_info.last_name.encode('utf-8'), paypal.payer.payment_method]


