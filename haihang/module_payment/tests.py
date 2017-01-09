# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.test import APITestCase
import json

class PaymentTests(APITestCase):
    """
    Test payment's API, include retrieve, post, pay, refund, and so on
    """
    # Mock Data from database: python manage.py dumpdata module_payment -a > fixtures/payment.json
    fixtures = ['fixtures/payment_account.json', 'fixtures/coupon.json', 'fixtures/payment.json']
    def test_create_payment(self):
        """
        创建支付单
        """
        data = {
            "payment_account_uuid": "0873366ca34211e6ab846451066036bd",
            "coupon_code": "JUI38K59",
            "payment_price": 10
        }
        response = self.client.post('/apis/v1/payments/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content['coupon_code'], 'JUI38K59')

    def test_create_payment_required(self):
        """
        创建支付单,必填验证
        """
        data = {
            "payment_account_uuid": "0873366ca34211e6ab846451066036bd",
            "coupon_code": "JUI38K59"
        }
        response = self.client.post('/apis/v1/payments/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_no_body(self):
        """
        创建支付单, 0输入
        """
        data = {}
        response = self.client.post('/apis/v1/payments/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_validate(self):
        """
        创建支付单, 有效性
        """
        data = {
            "payment_account_uuid": "0873366ca34211e6ab846451066036bdc",
            "coupon_code": "JUI38K59",
            "payment_price": 10
        }
        response = self.client.post('/apis/v1/payments/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_in_range(self):
        """
        创建支付单, 范围验证
        """
        data = {
            "payment_account_uuid": "0873366ca34211e6ab846451066036bd",
            "coupon_code": "JUI38K59",
            "payment_price": -10
        }
        response = self.client.post('/apis/v1/payments/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_payment_by_uuid(self):
        """
        查询支付单详情
        """
        response = self.client.get('/apis/v1/payments/2983ccf8-a348-11e6-a4ff-6451066036bd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['coupon_code'], 'DL8OFDDA')

    def test_get_payment_by_uuid_validate(self):
        """
        查询支付单详情,数据有效性
        """
        response = self.client.get('/apis/v1/payments/2983ccf8-a348-11e6-a4ff-6451066036bdc/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_payment_by_uuid_not_fount(self):
        """
        查询支付单详情, 404
        """
        response = self.client.get('/apis/v1/payments/2983ccf8-a348-11e6-a4ff-6451066036bc/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_payment_by_user(self):
        """
        获取支付单详情
        """
        response = self.client.get('/apis/v1/payments/user/c5071aba-a341-11e6-a4d5-6451066036bd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_payment_record(self):
        """
        查询支付单处理记录
        """
        response = self.client.get('/apis/v1/payments/2983ccf8-a348-11e6-a4ff-6451066036bd/record/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_payment_record_not_fount(self):
        """
        查询支付单处理记录, 404
        """
        response = self.client.get('/apis/v1/payments/2983ccf8-a348-11e6-a4ff-6451066036bc/record/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_get_payment_record_validate(self):
        """
        查询支付单处理记录,validate
        """
        response = self.client.get('/apis/v1/payments/2983ccf8-a348-11e6-a4ff-6451066036bdc/record/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)














    
