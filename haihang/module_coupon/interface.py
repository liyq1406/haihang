# -*- coding:utf-8 -*-

import logging
from django.utils import timezone
from module_coupon.models import Coupon, CouponUsage, CouponUser
from Payment.initConf import MODULE_COUPON
from Payment.util import get_kwargs

log = logging.getLogger('payment')

def check_coupon(coupon):
    """
    检查优惠码是否在有效期
    """
    now = timezone.now()
    try:
        # coupon = Coupon.objects.get(coupon_uuid=coupon_uuid)
        if  now <= coupon.valid_datetime_end and now >= coupon.valid_datetime_start:
            return True
        else:
            log.error('[coupon] coupon %s is not in the period of validity', coupon.coupon_code)
    except Exception as e:
        log.error('[coupon] %s valid error', coupon.coupon_code)
    return False

def binding_coupon(pk, payment_account_uuid, user_uuid):
    """
    绑定优惠码, 如果需要新增绑定关系, 需要传入优惠码, user_uuid, payment_account_uuid
    """
    if len(pk) == MODULE_COUPON['COUPON_CODE_LEN']:
        coupon_code_or_id = {'coupon_code': pk}
    else:
        coupon_code_or_id = {'coupon_uuid': pk}
    coupon_identify = get_kwargs(coupon_code_or_id)
    now = timezone.now()
    try:
        # 存在绑定关系, 检查剩余使用时间和次数是否满足
        coupon = Coupon.objects.get(**coupon_identify)
        coupon_user = CouponUser.objects.get(user_uuid=user_uuid,**coupon_identify)
        if coupon_user.using_count_left > 0 and now <= coupon.valid_datetime_end:
            log.info('[coupon] coupon %s is valid', coupon.coupon_code)
            return coupon_user, coupon
    except CouponUser.DoesNotExist:
        # 如果未发现绑定关系, 检查优惠码是否还有剩余可用人数, 如果有新建绑定关系
        coupon = Coupon.objects.get(**coupon_identify)
        if coupon.using_user_left > 0 and now <= coupon.valid_datetime_end:
            coupon_user = CouponUser(
                              coupon_uuid=coupon, 
                              user_uuid=user_uuid,
                              coupon_code=coupon.coupon_code,
                              coupon_type=coupon.coupon_type,
                              coupon_value=coupon.coupon_value,
                              payment_account_uuid=payment_account_uuid,
                              valid_datetime_start=coupon.valid_datetime_start,
                              valid_datetime_end=coupon.valid_datetime_end,
                              using_count_left=coupon.coupon_using_count)
            coupon_user.save()
            coupon.using_user_left = coupon.using_user_left -1
            coupon.save()
            log.info('[coupon] user_uuid %s binding coupon_uuid: %s', user_uuid, coupon.coupon_uuid)
            return coupon_user, coupon
    except Coupon.DoesNotExist:
        log.error('[coupon] coupon %s does not exist', pk)
    except Exception as e:
        log.error(e)
    log.error('[coupon] coupon %s is invalid', coupon_code_or_id)
    return False, False

def use_coupon(**kwargs):
    """
    优惠码使用接口, 需要提供coupon_code, PaymentAccount实例以及user_uuid, usage_source_type
    """
    user_uuid = kwargs.get('user_uuid')
    payment_account_uuid = kwargs.get('payment_account_uuid')
    coupon_code = kwargs.get('coupon_code')
    usage_source_type = kwargs.get('usage_source_type')
    usage_source_uuid = kwargs.get('usage_source_uuid')
    try:
        coupon = Coupon.objects.get(coupon_code=coupon_code)
        # coupon_user = CouponUser.objects.get(user_uuid=user_uuid, coupon_code=coupon_code)
        # if (usage_source_type=='account' and coupon.coupon_type != 'recharge') or \
        #    (usage_source_type=='payment' and coupon.coupon_type not in ('discount', 'reduce')):
        #     log.error('[coupon] coupon type error')
        #     return None
        # 生成使用记录
        coupon_usage = CouponUsage(
                           coupon_code=coupon.coupon_code,
                           coupon_uuid=coupon,
                           user_uuid=user_uuid,
                           payment_account_uuid=payment_account_uuid,
                           usage_source_type=usage_source_type,
                           usage_source_uuid=usage_source_uuid)
        # coupon_user.using_count_left = coupon_user.using_count_left - 1
        coupon_usage.save()
        log.info('[coupon] gen coupon usage for user_uuid: %s , coupon_code: %s', user_uuid, coupon_code)
        # coupon_user.save()
        return coupon_usage
    except Coupon.DoesNotExist:
        log.error('[coupon] coupon does not exist %s', coupon_code)
    except ValueError:
        log.error('[coupon] UUID error')
    except Exception as e:
        log.error(e)
        log.error('use coupon %s fail', coupon_code)
    return False
