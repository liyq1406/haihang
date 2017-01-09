# -*- coding:utf-8 -*-

from bill.util import get_record_bill, get_nopay_fee, create_bill, \
    change_recordbill
from module_payment_account.interface import change_balance
from price.util import gain_price_for_rancher
import datetime
import logging
import math
from bill.data_util import bill_is_exist

log = logging.getLogger('payment')


class Host(object):
    '''
    # 主机对象,  用于统计费用
    '''

    def __init__(self, user_uuid, host_userid, params):
        '''
        Constructor
        '''
        try:
            self.invalid = False
            self.user_uuid = user_uuid
            self.host_uuid = params.get('id', '')
            
            self.lifetime = int(params.get('lifetime', 0))
            self.host_userid = host_userid
            self.start_time = datetime.datetime.strptime(params['t'][0], "%Y-%m-%dT%H:%M:%SZ")

            hostInfo = params.pop('hostInfo', {})

            self.cpuCores = int(hostInfo.get('cpuCores', 0))
            self.memSize = int(hostInfo.get('memSize', 0))
            self.diskSize = int(hostInfo.get('diskSize', 0))
            self.name = hostInfo.get('hostname', '')
        except Exception, e:
            self.invalid = True
            log.error('[Host] init fail, host_userid=[%s],params=[%s],except=[%s]' % (host_userid, str(params), str(e)))

    def is_invalid(self):
        if self.invalid:
            return True

        self.price = self.get_price()
        self.paid_time = self.get_paid_time()
        self.nopay_time = self.get_nopay_time()

        if not self.price:
            log.error('get price fail')
            return True

        return False

    def get_price(self):
        if self.invalid:
            return None

        price = gain_price_for_rancher(cpu=self.cpuCores, mem=self.memSize, disk=self.diskSize)
        if price:
            return price
        else:
            log.error('[monitor] the price strategy is not existed:cpu=%d,mem=%d,disk=%d',
                      self.cpuCores, self.memSize, self.diskSize)
            return None

    def get_paid_time(self):
        bill_record = get_record_bill(host_uuid=self.host_uuid,
                                      name=self.name,
                                      cpu=self.cpuCores,
                                      mem=self.memSize,
                                      disk=self.diskSize)
        return bill_record.lifetime

    def get_nopay_time(self):
        return math.ceil((self.lifetime - self.paid_time) / 60) + 1

    def get_nopay_fee(self):
        # 月账单支付失败的总费用+上次生成账单到当前没有支付的费用
        nopay_time = self.get_nopay_time()
        return get_nopay_fee(user_id=self.host_userid) + nopay_time * self.price

    def is_deleted(self):
        # 通过主机开始时间和lifetime来判断主机是否停止了
        check_time = (datetime.datetime.now() - self.start_time)
        sec = check_time.days * 24 * 3600 + check_time.seconds
        if sec - self.lifetime > 3600 and self.lifetime != self.paid_time:
            return True

        return False

    def create_bill(self):
        current_month = datetime.datetime.now().month
        check_bill = bill_is_exist(user_uuid=self.user_uuid,month=current_month,host_uuid=self.host_uuid,pay_status=False,bill_status=True)
        if check_bill:
            new_bill = check_bill
        else:
            new_bill = create_bill(user_uuid=self.user_uuid,
                               host_uuid=self.host_uuid,
                               run_time=self.nopay_time,
                               name=self.name,
                               month=current_month,
                               total_fee=self.nopay_time * self.price)
        status = change_balance(self.user_uuid,
                                'bill',
                                -self.nopay_time * self.price,
                                new_bill.bill_uuid)

        if status is True:
            pay_status = True
            log.info('[bill] change_balance successful')
        else:
            pay_status = False
            log.info('[bill] change_balance faild')

        new_bill.pay_status = pay_status
        new_bill.run_time = self.nopay_time
        new_bill.total_fee = self.nopay_time * self.price
        new_bill.bill_account_time = datetime.datetime.now()
        new_bill.bill_status = False
        new_bill.save()

        change_recordbill(host_uuid=self.host_uuid, lifetime=self.lifetime)
