# encoding=utf-8
from models import Bill


def get_bill_byuserid(user_uuid, pay_status=False):
    """
    通过user_uuid获取该用户的所有账单
    """
    bills = Bill.objects.filter(user_uuid=user_uuid).filter(pay_status=pay_status)
    return bills


def get_allbill_byuserid(user_uuid):
    """
    通过user_uuid获取该用户的所有账单
    """
    return Bill.objects.filter(user_uuid=user_uuid)

def bill_is_exist(user_uuid,month,host_uuid,pay_status,bill_status):
    """
    查看账单是否存在
    """
    try:
        check_bill = Bill.objects.get(user_uuid=user_uuid,month=month,host_uuid=host_uuid,pay_status=pay_status,bill_status=bill_status)
        return check_bill
    except Bill.DoesNotExist:
        return 
    except Exception as e:
        log.error('[bill] bill_is_exist,{}'.format(e.__str__()))
        return 

    