# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.test import APITestCase
import json
import uuid

class PaymentAccountTests(APITestCase):
    """
    Test PaymentAccount's API, include retrieve, put, post, patch and user retrieve
    """
    # Mock Data from database: python manage.py dumpdata module_payment_account -a > fixtures/payment_account.json
    fixtures = ['fixtures/payment_account.json']
    def test_create_account(self):
        """
        测试创建账户功能
        """
        data = {
                "user_uuid": unicode(uuid.uuid1()),
                "credit": 200000,
                "balance": 20000,
                }
        response = self.client.post('/apis/v1/payment_accounts/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content['credit'], 200000)
        self.assertEqual(content['balance'], 20000)

    def test_create_account_required(self):
        """
        测试创建账户缺少必填项
        """
        data = {
                "credit": 200000,
                "balance": 20000,
                }
        response = self.client.post('/apis/v1/payment_accounts/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_no_body(self):
        """
        测试创建账户未输入任何信息
        """
        data = {}
        response = self.client.post('/apis/v1/payment_accounts/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_type_err(self):
        """
        测试创建账户输入数据类型错误
        """
        data = {
            "user_uuid": '01406842a34211e6b1d76451066036bdaa',
        }
        response = self.client.post('/apis/v1/payment_accounts/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_repeat(self):
        """
        测试创建账户user_uuid重复
        """
        data = {
            "user_uuid": 'c38413c8a34111e6a4d56451066036bd',
        }
        response = self.client.post('/apis/v1/payment_accounts/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_account_reange_err(self):
        """
        测试创建账户参数范围错误
        """
        data = {
            "user_uuid": '01406842a34211e6b1d76451066036bd',
            "credit": "-20",
        }
        response = self.client.post('/apis/v1/payment_accounts/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_list_account(self):
        """
        测试获取账户列表
        """
        response = self.client.get('/apis/v1/payment_accounts/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_get_account_by_accountuuid(self):
        """
        测试使用获取账户详情
        """
        response = self.client.get('/apis/v1/payment_accounts/01406842a34211e6b1d76451066036bd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_by_accountuuid_type_err(self):
        """
        获取账户详情uuid错误
        """
        response = self.client.get('/apis/v1/payment_accounts/01406842a34211e6b1d76451066036bdc/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_account_by_accountuuid_not_found(self):
        """
        获取账户详情uuid不存在
        """
        response = self.client.get('/apis/v1/payment_accounts/01406842a34211e6b1d76451066036bc/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_account_by_useruuid(self):
        """
        获取账户详情
        """
        response = self.client.get('/apis/v1/payment_account/user/?user_uid=c38413c8a34111e6a4d56451066036bd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_by_useruuid(self):
        """
        获取账户详情uuid错误
        """
        response = self.client.get('/apis/v1/payment_account/user/?user_uuid=c38413c8a34111e6a4d56451066036bdd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_patch_account(self):
        """
        修改账户信息
        """
        data = {
                "credit": 0,
                "is_delete": "true"
                }
        response = self.client.patch('/apis/v1/payment_accounts/01406842a34211e6b1d76451066036bd/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['credit'], 0)
        self.assertEqual(content['is_delete'], True)

    def test_patch_account_range_err(self):
        """
        修改账户信息,数据范围
        """
        data = {
                "credit": "-20",
                }
        response = self.client.patch('/apis/v1/payment_accounts/01406842a34211e6b1d76451066036bd/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_patch_account_not_found(self):
        """
        修改账户信息,存在性
        """
        data = {
                "credit": 0,
                "is_delete": "true"
                }
        response = self.client.patch('/apis/v1/payment_accounts/01406842a34211e6b1d76451066036bc/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AccountRecordTests(APITestCase):
    """
    Test AccountRecord's API, include list and user list. 
    """
    fixtures = ['fixtures/payment_account.json']

    def test_get_record_by_accountuuid(self):
        """
        Ensure get a payment account's record func
        """
        response = self.client.get('/apis/v1/account_records/01406842a34211e6b1d76451066036bd/?limit=10&order_by=create_time&desc=0')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_record_by_accountuuid_valide(self):
        """
        Ensure get a payment account's record func
        """
        response = self.client.get('/apis/v1/account_records/01406842a34211e6b1d76451066036bdd/?limit=10&order_by=create_time&desc=0')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_record_by_useruuid(self):
        """
        Ensure get a payment account's record func
        """
        response = self.client.get('/apis/v1/account_record/user/?user_uuid=c38413c8a34111e6a4d56451066036bd/?limit=100&order_by=modify_balance')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_record_by_useruuid_valide(self):
        """
        Ensure get a payment account's record func
        """
        response = self.client.get('/apis/v1/account_record/user/?user_uuid=c38413c8a34111e6a4d56451066036bdd/?limit=100&order_by=modify_balance')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
