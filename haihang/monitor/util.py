# -*- coding:utf-8 -*-
from Payment.initConf import ENV_INIT
from Payment.util import get_config_value
from module_payment_account.interface import get_account_by_user_uuid, \
    list_account
from monitor.host import Host
from monitor.models import AlertRecord
import Queue
import datetime
import logging
import requests
import threading

# 测试的用户账号表


log = logging.getLogger('payment')


def create_url(user_id):
    """
    # 生成url
    :param url:
    :return:
    """
    rancher_url = ENV_INIT['RANCHER_URL'] + user_id + "/hosts"
    return rancher_url


# 估算剩余使用时长
def reckon_remaind(user_uuid, num=0, minute_price=0):
    """
    # user_uuid,minute_price
    # 通过user_uuid估算剩余使用天数(天）,
    """

    log.info('[monitor] reckon_remaind user_uuid:[%s],num=[%s],minute_price[%s]' % (user_uuid, num, minute_price))
    # 默认值
    data_dic = {'last_days': 0, 'active_money': 0, 'host_num':1}

    try:
        num = int(num)
        minute_price = float(minute_price)
        host_url = create_url('1a' + user_uuid)
    except Exception:
        log.error('[monitor] reckon_remaind parameter is in invalid')
        return data_dic

    # 查看用户账户余额
    account = get_account_by_user_uuid(user_uuid=user_uuid)
    if not account:
        return data_dic

    strategy = get_config_value('strategy')
    if strategy == 'NO_BALANCE_LEFT':
        credit = 0
    else:
        credit = get_config_value('credit', 0)

    # 如果余额加信用额度小于0，就直接返回    
    if account.balance + credit <= 0:
        log.info('[monitor] reckon_remaind user:%s,account.balance:%s,credit:%s balance \
        less than 0' % (user_uuid, account.balance, credit))
        data_dic['active_money'] = account.balance + credit
        return data_dic

    try:
        hosts_all = requests.get(host_url, timeout=10).json()
        log.debug('[monitor] get data from [%s]return[%s]' % (host_url, str(hosts_all)))
    except Exception:
        log.error('[monitor] util.run_task:connect beancounter timeout or refused')
        return data_dic

    host_userid = ''
    if isinstance(hosts_all, dict) and 'id' in hosts_all:
        host_userid = hosts_all['id']

    if not host_userid:
        return data_dic

    # 没有主机的情况
    if 'hosts' not in hosts_all or len(hosts_all['hosts']) == 0:
        data_dic['host_num'] = 0
        if num and minute_price:
            data_dic['last_days'] = round(float(account.balance + credit) / (minute_price * num * 60 * 24), 2)
        else:
            data_dic['last_days'] = 0

        data_dic['active_money'] = account.balance
        log.debug('[monitor] [reckon_remaind] the user:%s no host. last_days=%s', user_uuid, data_dic['last_days'])
        return data_dic

    no_pay_fee = 0
    price_minute = 0
    for host in hosts_all['hosts']:
        hostObj = Host(user_uuid, host_userid, host)
        if hostObj.is_invalid():
            log.error('[monitor] The host is invalid')
            continue

        price_minute += hostObj.price
        no_pay_fee += hostObj.get_nopay_fee()
        # 如果主机删除，生成账单并扣费
        if hostObj.is_deleted():
            hostObj.create_bill()
            log.info('[monitor][reckon_remaind] the user:%s\'s host:%s is deleted', user_uuid, hostObj.host_uuid)

    # 实际可用余额
    active_money = account.balance - no_pay_fee

    # 实际可用余额小于0，直接返回
    if active_money <= 0:
        data_dic['active_money'] = active_money
        log.info('[monitor] [reckon_remaind] the user:%s active_money=%s', user_uuid, active_money)
        return data_dic

    if num and minute_price:
        # 如果是check_account接口来调用，那么每分钟价格需要加上需要开启主机的数量和每种规格的价格
        price_minute = price_minute + minute_price * num

    if price_minute > 0:
        last_days = round(float(active_money + credit) / (price_minute * 60 * 24), 2)
    else:
        last_days = 0

    data_dic['last_days'] = last_days
    data_dic['active_money'] = active_money

    return data_dic

def get_user_name(user_uuid):
    index = ENV_INIT['USER_SYSTEM_URL'].rfind('/')
    url = ENV_INIT['USER_SYSTEM_URL'][:index] + '/userInfoByEvnid/' + user_uuid
    try:
        user_data = requests.get(url, timeout=10).json()
        log.debug('get_user_name from user system[%s] return[%s]'%(url, str(user_data)))
    except Exception as e:
        log.error('[monitor] get user_name by env id. {}'.format(e.__str__()))
        return ''
    
    if isinstance(user_data, dict):
        return user_data.get('data', {}).get('name','')
    return ''


def alert_message(user_uuid, level_days, notify_strategy=None):
    """
    # 调用通知接口
    """
    data = {}
    data['user_name'] = get_user_name(user_uuid)
    data['level'] = 'INFO'
    data['module'] = 'BL'
    data['msg_title'] = 'account alert'
    data['msg_content'] = '您的账户余额已不足，预估可使用[%s]天' % (level_days)
    data['msg_url'] = ''

    if notify_strategy is None:
        data['is_phone'] = 'True' if get_config_value('sms_notify') else 'False'
        data['is_email'] = 'True' if get_config_value('email_notify') else 'False'
    elif notify_strategy == 0:
        data['is_phone'] = 'False'
        data['is_email'] = 'False'
    elif notify_strategy == 1:
        data['is_phone'] = 'False'
        data['is_email'] = 'True'
    elif notify_strategy == 2:
        data['is_phone'] = 'True'
        data['is_email'] = 'False'
    else:
        data['is_phone'] = 'True'
        data['is_email'] = 'True'

    alert_url = ENV_INIT['ALERT_URL']

    try:
        alert_return = requests.post(alert_url, data=data, timeout=10)
    except requests.exceptions.RequestException:
        log.error('[monitor.alert_message] connect {} error'.format(alert_url))
        return

    log.debug("[monitor.alert_message] call the message api [%s]" % (alert_url))
    if alert_return.status_code == 200:
        log.info("[monitor.alert_message] send message[%s]success" % (str(data)))
    else:
        log.error("[monitor.alert_message] send message[%s]fail" % (str(data)))


def create_alertrecord(user_id, alert_number):
    """
    create AlertRecord object
    :return:
    """
    alert_record = AlertRecord()
    alert_record.user_id = user_id
    alert_record.alert_number = alert_number
    alert_record.save()


def check_alert_time(user_uuid, check_alert, alert_number, level_days, notify_strategy=None):
    """
    :param check_alert:
    :return: 
    """
    if check_alert.count() == 0:
        create_alertrecord(user_uuid, alert_number)
        alert_message(user_uuid, level_days, notify_strategy)
    else:
        alertObj = check_alert[0]
        if alertObj.alert_number != alert_number:
            alert_message(user_uuid, level_days, notify_strategy)
            check_alert1 = alertObj
            check_alert1.alert_number = alert_number
            check_alert1.save()


def get_alert_strategy():
    sms_notify = int(get_config_value('sms_notify'))
    email_notify = int(get_config_value('email_notify'))
    if sms_notify == 0 and email_notify == 0:
        notify_strategy = 0
    elif sms_notify == 0 and email_notify == 1:
        notify_strategy = 1
    elif sms_notify == 1 and email_notify == 0:
        notify_strategy = 2
    else:
        notify_strategy = 3
    return notify_strategy


def run_task(one):
    """
    # 对每个用户去进行监控
    :param one:
    :return:
    """
    days_dic = reckon_remaind(one.user_uuid)
    if days_dic and 'last_days' in days_dic:
        days = days_dic['last_days']
        # 用户没有主机时候不用监控
        if days <= 0:
            log.info('[monitor][run_task] the user:%s no host.Need not monitor', one.user_uuid)
            return
        check_alert = AlertRecord.objects.filter(user_id=one.user_uuid)
        minor_alarm_days = get_config_value('minor_alarm_days')
        critical_alarm_days = get_config_value('critical_alarm_days')
        emergency_alarm_days = get_config_value('emergency_alarm_days')
        
        if days > minor_alarm_days:
            log.info('[monitor] run_task.the account is enough')
            return
        if days <= minor_alarm_days and days > critical_alarm_days:
            check_alert_time(one.user_uuid, check_alert, 1, days)

        elif days <= critical_alarm_days and days > emergency_alarm_days:
            check_alert_time(one.user_uuid, check_alert, 2, days)

        elif days <= emergency_alarm_days:
            check_alert_time(one.user_uuid, check_alert, 3, days)
        log.info('[monitor][run_task] the user:%s\'s account can support %s days.', one.user_uuid, days)


class account_consumer(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            one = self._queue.get()
            if isinstance(one, str) and one == 'quit':
                break
            try:
                run_task(one)
            except Exception as e:
                log.error('[monitor] 额度监控执行失败:{}'.format(e.__str__()))


def accountmonitor():
    """
    # 额度监控  每个月月底结算当月账单
    # 先计算用户所有未支付账单的总费用，再用账户可用余额减去总费用与设定的警戒比较
    # 调用获取所有用户账户接口
    """

    accounts = list_account()
    log.info('[monitor] accountmonitor.monitor\' accounts:{}'.format(accounts.count()))
    if accounts.count() > 0:
        queue = Queue.Queue()
        worker_threads = build_worker_pool(queue, 1)
        start_time = datetime.datetime.now()
        for one in accounts:
            queue.put(one)
        for worker in worker_threads:
            queue.put('quit')
        for worker in worker_threads:
            worker.join()
        log.info('[monitor] accountmonitor.Time taken:{}'.format(datetime.datetime.now() - start_time))


def build_worker_pool(queue, size):
    workers = []
    for _ in range(size):
        worker = account_consumer(queue)
        worker.start()
        workers.append(worker)
    return workers
