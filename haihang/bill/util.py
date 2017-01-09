# -*- coding:utf-8 -*-
import redis
from Payment.initConf import ENV_INIT
from models import Bill, BillRecord, MonthAccountRecord
from module_payment_account.interface import change_balance, list_account
from price.util import gain_price_for_rancher
import datetime
import logging
import requests
import threading
import Queue
import math

account_lock = threading.Lock()

log = logging.getLogger('payment')


def create_url(user_id):
    """
    生成url
    :param url:
    :return:
    """
    rancher_url = ENV_INIT['RANCHER_URL'] + user_id + "/hosts"
    return rancher_url


def get_nopay_fee(user_id):
    """
    获取支付失败的账单的总费用
    :param host_uuid:
    :return:
    """
    try:
        # 找出支付失败的月账单,
        bills = Bill.objects.filter(user_uuid=user_id, pay_status=False, bill_status=False)
        total_fee = 0
        for bill in bills:
            total_fee += bill.total_fee
        return total_fee
    except Exception:
        return None


def get_nopay_bill(user_id):
    """
    获取用户支付失败的月账单列表
    :param user_id:
    :return:
    """
    try:
        fail_pay_bills = Bill.objects.filter(user_uuid=user_id, pay_status=False)
        return fail_pay_bills
    except Exception:
        return None


def get_record_bill(host_uuid, name, cpu, mem, disk):
    """
    获取主机记录表
    :param host_uuid:
    :return:
    """
    try:
        record_bill = BillRecord.objects.get(host_uuid=host_uuid)
    except BillRecord.DoesNotExist:
        create_record = BillRecord(host_uuid=host_uuid, name=name, cpu=cpu, mem=mem, disk=disk, lifetime=0)
        create_record.save()
        return create_record
    except BillRecord.MultipleObjectsReturned:
        log.error('[bill] get_record_bill error.the host_uuid:{} has more  than one BillRecord'.format(host_uuid))
        return
    return record_bill


def change_redis_bill_record(host_uuid, lifetime):
    """

    :return:
    """
    try:
        r = redis.Redis(host=ENV_INIT['REDIS_HOST'], port=ENV_INIT['REDIS_PORT'], db=ENV_INIT['REDIS_DB'])
        r.hset('host' + host_uuid, lifetime)

    except Exception as e:
        log.error('[bill] change_redis_bill_record error.{}'.format(e.__str__()))


def change_recordbill(host_uuid, lifetime):
    """
    改变账单记录表
    :param host_uuid:
    :param lifetime:
    :return:
    """
    try:
        record_bill = BillRecord.objects.get(host_uuid=host_uuid)
        record_bill.lifetime = lifetime
        record_bill.save()
    except BillRecord.MultipleObjectsReturned:
        log.error('[bill] the host_uuid:{} record more than one BillRecord.'.format(host_uuid))
    except Exception as e:
        log.error('[bill] change_recordbill error.{}'.format(e.__str__()))


def create_bill(user_uuid, name, host_uuid, run_time, month, total_fee):
    try:
        new_bill = Bill()
        new_bill.user_uuid = user_uuid
        new_bill.host_uuid = host_uuid
        new_bill.run_time = run_time
        new_bill.month = month
        new_bill.name = name
        new_bill.total_fee = total_fee
        new_bill.bill_account_time = datetime.datetime.now()
        new_bill.save()
        return new_bill
    except Exception as e:
        log.error('[bill] create_bill error.{}'.format(e.__str__()))
        return None


def check_host_bill(host, user_name, choice):
    """
    通过主机id来生成账单，如果是用户查询不需要结算，如果是生成月账单，则需要结算
    :param kwargs:
    :return:
    """
    cpu = host['hostInfo']['cpuCores']
    mem = host['hostInfo']['memSize']
    disk = host['hostInfo']['diskSize']
    name = host['hostInfo'].get('hostname', '')
    # 获取上次结算后的lifetime,不存在则返回新的账单记录表
    bill_record = get_record_bill(host_uuid=host['id'],name=name,cpu=cpu, disk=disk, mem=mem)
    current_month = datetime.datetime.now().month
    last_month = 12 if current_month == 1 else current_month - 1
    # 当主机还在运行时候需要生成账单,如果是用户查询不需要结算，如果是生成月账单，则需要结算
    if host['lifetime'] > bill_record.lifetime:
        # 只统计没有删除的主机
        price = gain_price_for_rancher(cpu=cpu, mem=mem, disk=disk)
        if price:
            # 主机从上次结帐到当前还没结帐的时间
            run_time = math.ceil((host['lifetime'] - bill_record.lifetime) / 60) + 1
            fee = run_time * price
            # 当是月账单定时任务，需要结算
            if choice == "month_account":
                # 先查看有没有该主机的上个月账单(当用户在查看账单时候会根据用户查询时间生成账单,没有扣费),并且是没有支付的,bill_status=False
                try:

                    check_bill = Bill.objects.get(user_uuid=user_name, host_uuid=host['id'], month=last_month, \
                                                  pay_status=False,
                                                  bill_status=True)
                except Bill.DoesNotExist:
                    log.info('[bill] build month bill. bill not exist. create new bill ')
                    # mutex.acquire(1)
                    # if mutex.acquire(1):
                    new_bill = Bill(user_uuid=user_name, name=name, host_uuid=host['id'],
                                    run_time=run_time, month=last_month, total_fee=fee)
                    new_bill.save()
                    log.info('[bill] create a new month bill:{}'.format(new_bill.bill_uuid))

                    status = change_balance(user_name, 'bill', -fee, new_bill.bill_uuid)

                    if status is True:
                        pay_status = True
                        log.info('[bill] change_balance successful.modify balance:{}'.format(-fee))
                    else:
                        pay_status = False
                        log.info('[bill] change_balance faild')

                    new_bill.pay_status = pay_status
                    new_bill.bill_account_time = datetime.datetime.now()
                    new_bill.bill_status = False
                    new_bill.save()
                    change_recordbill(host_uuid=host['id'], lifetime=host['lifetime'])
                    return
                except Exception as e:
                    log.error('[bill] check_host_bill other error:{}'.format(e.__str__()))
                    return

                status = change_balance(user_name, 'bill', -fee, check_bill.bill_uuid)
                if status is True:
                    pay_status = True
                    log.info('[bill] no pay bill:{}'.format(check_bill.bill_uuid))
                    log.info('[bill] change_balance successful.modify balance:{}'.format(-fee))
                else:
                    pay_status = False
                    log.info('[bill] change_balance faild')
                # mutex.acquire()
                check_bill.pay_status = pay_status
                check_bill.run_time = run_time
                check_bill.total_fee = fee
                check_bill.bill_account_time = datetime.datetime.now()
                check_bill.bill_status = False
                check_bill.save()
                change_recordbill(host_uuid=host['id'], lifetime=host['lifetime'])

            else:
                # 先查看有没有该主机的当月账单(当用户在查看账单时候会根据用户查询时间生成账单,没有扣费),并且是没有支付的,bill_status=False
                try:
                    check_bill = Bill.objects.get(host_uuid=host['id'], month=current_month,
                                                  pay_status=False,
                                                  bill_status=True)
                    check_bill.run_time = run_time
                    check_bill.total_fee = fee
                    check_bill.save()
                except Bill.DoesNotExist:
                    new_bill = Bill(user_uuid=user_name, host_uuid=host['id'], name=name
                                    , run_time=run_time, month=current_month, total_fee=fee)
                    new_bill.save()
                    log.info('[bill] user see bill.create a new month bill')
                except Exception as e:
                    log.error('[bill] check_host_bill more than one bill meet the condition:{}'.format(e.__str__()))
                    return
        else:
            log.error('[bill] the price startegy is not existed.cpu=%d,mem=%d,disk=%d', \
                      cpu, mem, disk)


mutex = threading.Lock()


class MonthAccountConsumer(threading.Thread):
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
                run_task(account)
            except Exception as e:
                log.error('[bill] 月账单结算失败:{}'.format(e.__str__()))
                return


def build_worker_pool(queue, size):
    """
    仓库
    :param queue:
    :param size:
    :return:
    """
    workers = []
    for _ in range(size):
        worker = MonthAccountConsumer(queue)
        worker.start()
        workers.append(worker)
    return workers


def run_task(account):
    # 通过用户到rancher获取该用户的主机信息
    log.debug('month_acccount run task start. account:[%s]' % (account))
    host_url = create_url('1a' + account.user_uuid)
    try:
        hosts_all = requests.get(host_url, timeout=10).json()
    except requests.exceptions.RequestException:
        log.error('[bill] util.run_task:connect beancounter timeout or refused')
        current_month = datetime.datetime.now().month
        last_month = 12 if current_month == 1 else current_month - 1
        record = MonthAccountRecord.objects.filter(user_id=account.user_uuid, month=last_month,
                                                   pay_status=False)
        if record.count() == 0:
            record_create = MonthAccountRecord(user_id=account.user_uuid, month=last_month)
            record_create.save()
        return

    if 'hosts' in hosts_all:
        hosts = hosts_all['hosts']
        user_name = hosts_all['id'][2:]
        for host in hosts:
            check_host_bill(host=host, user_name=user_name, choice='month_account')


def month_account():
    """
     对所有账户进行结算
    每个月的1号结算账单上个月账单
    :param bill_uuid:
    :return:
    """
    # ------------------------------------
    # 调用获取所有用户账户接口
    log.info('[bill] month_account start.....')
    accounts = list_account()
    log.info('[bill] month_account.len(accounts):{}'.format(accounts.count()))
    # ------------------------------------
    if accounts.count() > 0:
        # 遍历每一个用户
        queue = Queue.Queue()
        worker_threads = build_worker_pool(queue, 1)
        start_time = datetime.datetime.now()
        for account in accounts:
            queue.put(account)
        for worker in worker_threads:
            queue.put('quit')
        for worker in worker_threads:
            worker.join()
        log.info('[bill] month_account,Time taken:{}'.format(datetime.datetime.now() - start_time))


def get_bill_byuserid(user_uuid, pay_status=False):
    """
    通过user_uuid获取该用户的所有账单
    """
    bills = Bill.objects.filter(user_uuid=user_uuid).filter(pay_status=pay_status)
    if bills.count() > 0:
        return bills
    else:
        return None
