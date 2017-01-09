# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.test import APITestCase
import json


class BillTest(APITestCase):
    """
    test bill's API,
    """
    # fixtures为测试用例所用的数据，python manage.py dumpdata bill -a > fixtures/bill.json
    fixtures = ['fixtures/bill.json', 'fixtures/account.json']

    def test_get_bills_bycondition(self):
        """
        测试传入所有参数
        :return:
        """
        response = self.client.get(
            '/apis/v1/bills/get_bills_bycondition/?bill_uuid=7562f924-ca90-11e6-904c-3423875a370b&\
            user_uuid=121&bill_account_time__gte=2016-11-30%2016:0:0Z&\
            bill_account_time__lte=2016-12-30%2016:0:0Z&limit=10&offset=0&pay_status=1')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content['content']), 1)
        self.assertEqual(content.get['content'][0]['user_uuid'], '121')

    def test_get_bills_bycondition_error(self):
        """
        测试传入参数key错误
        :return:
        """
        response = self.client.get(
            '/apis/v1/bills/get_bills_bycondition/?bil_account_time__gte=2016-11-30%2016:0:0Z&\
            bill_account_time__lte=2016-12-30%2016:0:0Z&limit=10&offset=0&pay_status=1')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content['content']), 10)

    def test_get_bills_bycondition_timeerror(self):
        """
        测试传入时间格式错误
        :return:
        """
        response = self.client.get(
            '/apis/v1/bills/get_bills_bycondition/?bill_account_time__gte=2016-11-30%2016:0:0Z&\
            bill_account_time__lte=2016-12-30%2016:0:0Z&limit=10&offset=0&pay_status=1')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 2)
        self.assertEqual(content['content'][0]['user_uuid'], '1271')

    def test_get_bills_bycondition_meth(self):
        """
        测试请求方式错误
        :return:
        """
        data = {
            'bill_uuid': "7562f922-ca90-11e6-904c-3423875a370b",
            'user_uuid': "121",
            'host_uuid': "4ee548ae-3e08-4d2a-8aa9-5008467bf091",
            'pay_status': 1,
            'bill_account_time__gte': "2016-11-30 16:0:0Z",
            'bill_account_time__lte': "2016-12-30 16:0:0Z"
        }
        response = self.client.post('/apis/v1/bills/get_bills_bycondition/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


