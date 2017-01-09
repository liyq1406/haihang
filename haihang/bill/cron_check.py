# -*- coding:utf-8 -*-
from module_payment_account.interface import change_balance, list_account
from bill.util import get_nopay_bill, create_url, check_host_bill
import logging
import threading
import Queue
import requests
import datetime
from models import MonthAccountRecord

log = logging.getLogger('payment')


class CheckFailPayConsumer(threading.Thread):
    """
    消费者
    """

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            account = self._queue.get()
            if isinstance(account, str) and account == 'quit':
                break
            try:
                run_check_task(account)
            except Exception as e:
                log.error('[bill] check month account fail,{}'.format(e.__str__()))


def build_worker_pool(queue, size):
    """
    仓库
    :param queue:
    :param size:
    :return:
    """
    workers = []
    for _ in range(size):
        worker = CheckFailPayConsumer(queue)
        worker.start()
        workers.append(worker)
    return workers


def run_check_task(account):
    """
    分配给每个线程的任务
    :param account:
    :return:
    """
    fail_pay_bill = get_nopay_bill(account.user_uuid)
    if fail_pay_bill.count() == 0:
        log.info('[bill] not found fail paid month bill')
    for bill in fail_pay_bill:
        log.info('[bill] 发现了一个月账单支付失败的账单')
        
        status = change_balance(account.user_uuid, 'bill', -bill.total_fee, bill.bill_uuid)
        if status is True:
            log.info('[bill] check a fail account bill successful.modify_balance:{}'.format(-bill.total_fee))
            bill.pay_status = True
            bill.save()


def check_fail_accountor():
    """
    每天去检查扣款失败的账单
    然后重新支付
    :return:
    """
    log.info('check_fail_accountor start....')
    accounts = list_account()
    if accounts.count() > 0:
        queue = Queue.Queue()
        worker_threads = build_worker_pool(queue, 1)

        for account in accounts:
            queue.put(account)
        for worker in worker_threads:
            queue.put('quit')
        for worker in worker_threads:
            worker.join()


# -----------------------------查看是否有没有生成月账单失败的用户---------------------------------------------
class CheckMonthBillConsumer(threading.Thread):
    """
    消费者
    """

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while True:
            account = self._queue.get()
            if isinstance(account, str) and account == 'quit':
                break
            try:
                check_bill_task(account)
            except Exception as e:
                log.error('[bill] check month bill fail.{}'.format(e.__str__()))


def check_bill_task(account):
    host_url = create_url('1a' + account)
    try:
        hosts_all = requests.get(host_url, timeout=10).json()
    except requests.exceptions.RequestException:
        log.error('[bill] check month bill fail. connect beancounter timeout or refused!')
        return

    if 'hosts' in hosts_all:
        hosts = hosts_all['hosts']
        user_name = hosts_all['id'][2:]
        try:
            for host in hosts:
                check_host_bill(host=host, user_name=user_name, choice='month_account')
        except Exception as e:
            log.error('[bill] check bill task:{}'.format(e.__str__()))
            return
        current_month = int(datetime.datetime.now().strftime('%m'))
        last_month = 12 if current_month == 1 else current_month - 1
        month_record = MonthAccountRecord.objects.filter(month=last_month, pay_status=False)
        for one in month_record:
            one.pay_status = True
            one.save()


def bill_worker_pool(queue, size):
    """
    仓库
    :param queue:
    :param size:
    :return:
    """
    workers = []
    for _ in range(size):
        worker = CheckMonthBillConsumer(queue)
        worker.start()
        workers.append(worker)
    return workers


def check_month_account():
    """
    对月账单结算失败的用户进行重新结算
    :param bill_uuid:
    :return:
    """
    # ------------------------------------
    # 调用获取所有用户账户接口
    # 调用获取所有用户账户接口
    log.info('check_month_account start.....')
    current_month = int(datetime.datetime.now().strftime('%m'))
    last_month = 12 if current_month == 1 else current_month - 1
    record = set(MonthAccountRecord.objects.filter(pay_status=False, month=last_month).values_list('user_id'))
    accounts = []

    for _ in record:
        accounts.append(_[0])
    log.info('[bill] check月账单结算失败任务开始.len(accounts):{},accounts list:{}'.format(len(accounts), accounts))
    # ------------------------------------
    if accounts:
        # 遍历每一个用户
        queue = Queue.Queue()
        worker_threads = bill_worker_pool(queue, 1)
        start_time = datetime.datetime.now()
        for account in accounts:
            queue.put(account)
        for worker in worker_threads:
            queue.put('quit')
        for worker in worker_threads:
            worker.join()
            # log.debug(Time_taken=datetime.datetime.now()-start_time)
