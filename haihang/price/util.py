# encoding=utf-8
import logging
import pytz
log = logging.getLogger('payment')
from price.models import Price
import datetime


def gain_price(cpu, mem, disk):
    current_date = datetime.datetime.now()
    price_obj = Price.objects.filter(cpu=cpu, mem=mem, disk=disk, effective_date__lte=current_date). \
        order_by('-effective_date')
    if price_obj.count() == 0:
        return None
    else:
        return price_obj[0].price


def gain_price_for_rancher(cpu, mem, disk):
    current_date = datetime.datetime.now(pytz.timezone('UTC'))
    # current_date = datetime.datetime.now().replace(tzinfo=None)
    price_obj = Price.objects.filter(cpu=cpu, mem__gte=mem, mem__lte=mem + 500, disk__gte=disk/1024, disk__lte=disk/1024 + 2,
                                  effective_date__lte=current_date).order_by('-effective_date')
    if price_obj.count() == 0:
        return None
    return price_obj[0].price


def gain_price_byuuid(price_uuid):
    try:
        price = Price.objects.get(price_uuid=price_uuid)
        return price
    except Price.DoesNotExist:
        return None
    except ValueError:
        return 'ValueError'
    except Exception as e:
        return 'other'
