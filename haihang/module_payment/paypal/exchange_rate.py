# -*- coding:utf-8 -*-

from urllib import urlopen
import re

def get_change_rate():
    """
    获取当前人民币汇率
    1 USD = return CNY
    """
    try:
        fp = urlopen('http://webforex.hermes.hexun.com/forex/quotelist?code=FOREXUSDCNY&column=code,price')
        rate = fp.read().decode()
        fp.close()
        rate = re.search(r'[0-9]{5}', rate)
        return int(rate.group()) / 10000.0
    except Exception as e:
        return False

def CNY_USD(yuan):
    """
    人民币换算美元
    return dollar, rate
    """
    rate = get_change_rate()
    dollar = round(yuan / rate, 2)
    return dollar, rate

def USD_CNY(dollar):
    """
    美元换算人民币
    return yuan, rate
    """
    rate = get_change_rate()
    yuan = round(dollar * rate, 2)
    return yuan, rate