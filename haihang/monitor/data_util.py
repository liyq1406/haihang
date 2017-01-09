# -*- coding:utf-8 -*-

from monitor.models import AlertRecord

def reset_monitor(user_id):
    """
    当用户充值了后，将告警次数归零
    """
    try:
        alert = AlertRecord.objects.get(user_id=user_id)
        alert.alert_number = 0
        alert.save()
        return True
    except AlertRecord.DoesNotExist:
        return False