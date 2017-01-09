# -*- coding:utf-8 -*-
"""
供项目内不同app调用
"""

import logging
from module_payment_account.models import PaymentAccount, AccountRecord
from Payment.util import get_config_value
from monitor.data_util import reset_monitor
from django.db.transaction import TransactionManagementError

log = logging.getLogger('payment')

def list_account():
    """
    # 列出所有账户 
    """
    return PaymentAccount.objects.all()

def change_balance(user_uuid, modify_source_type, modify_balance, modify_source_uuid, payment_account_uuid=None):
    """
    # 账户变更接口, 变更用户额度以及可用性. 
    {
        "payment_account_uuid":"68c4add4-9f14-11e6-80d3-6451066036bd",
        "modify_balance":-100,
        "modify_source_type": "bill",
        "modify_source_uuid":"68c4add4-9f14-11e6-80d3-6451066036bd"
    }
    """
    try:
        if user_uuid:
            paymentAccount = PaymentAccount.objects.get(user_uuid=user_uuid)
        elif payment_account_uuid:
            paymentAccount = PaymentAccount.objects.get(payment_account_uuid=payment_account_uuid)
        else:
            log.error('[account] no param payment_account_uuid or user_uuid')
            return False
    except PaymentAccount.DoesNotExist:
        log.error('[account] %s not found', payment_account_uuid or user_uuid)
        return False
    
    if modify_balance < 0 and modify_source_type not in ('bill', 'admin', 'refund'):
        log.error('[account] modify_source_type not match modify_balance')
        return False
    
    elif modify_balance > 0 and modify_source_type not in ('payment', 'admin'):
        log.error('[account] modify_source_type not match modify_balance')
        return False
        
    # 基于策略以及额度判断
    balance = paymentAccount.balance + modify_balance
    if get_config_value('strategy', 'NO_BALANCE_LEFT') == 'NO_BALANCE_LEFT':
        is_valid = False if balance < 0 else True
        
    if get_config_value('strategy', 'NO_BALANCE_LEFT') == 'NO_CREDIT_LEFT':
        is_valid = False if (balance + paymentAccount.credit) < 0 else True
        
    try:
        accountRecord = AccountRecord(
                            payment_account_uuid=paymentAccount,
                            modify_balance=modify_balance,
                            modify_source_type=modify_source_type,
                            modify_source_uuid=modify_source_uuid)
        # 用户额度变更
        paymentAccount.balance = balance
        paymentAccount.is_valid = is_valid
        paymentAccount.save()
        # 变更记录生成
        accountRecord.save()
        log.info('[account] change balance from modify_source_uuid %s success', modify_source_uuid)
        if modify_balance > 0:
            reset_monitor(user_id=paymentAccount.user_uuid)
            log.info('[account] notify monitor reset alarm times')
        return True
    except TransactionManagementError:
        log.error('[account] change balance from modify_source_uuid %s error', modify_source_uuid)
        return False

def get_account_by_user_uuid(**kwargs):
    """
    # 使用user_uuid查询账户详情, user_uuid不存在时使用该uuid以及默认配置创建新账户
    """
    if not is_valid_user_uuid(kwargs.get('user_uuid')):
        return False
    try:
        queryset = PaymentAccount.objects.get(user_uuid=kwargs.get('user_uuid'))
    except PaymentAccount.DoesNotExist:
        # 查询不到该用户时使用默认配置创建新账号
        queryset = PaymentAccount(user_uuid=kwargs['user_uuid'], credit=get_config_value('credit', 0))
        queryset.save()
        log.info('[account] create payment account %s use default settings.', kwargs.get('user_uuid'))
    return queryset

def is_valid_user_uuid(user_uuid):
    return user_uuid.isdigit()
    
