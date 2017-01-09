# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.test import APITestCase
import json

class CouponTests(APITestCase):
    """
    Test coupon's API, include retrieve, post
    """
    # Mock Data from database: python manage.py dumpdata module_coupon -a > fixtures/coupon.json
    fixtures = ['fixtures/payment_account.json', 'fixtures/coupon.json']
    def test_list_all_coupon(self):
        response = self.client.get('/apis/v1/coupons/list_all/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_list_all_valid_coupon(self):
        response = self.client.get('/apis/v1/coupons/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_create_coupon(self):
        """
        测试创建优惠码功能
        """
        data = {
            'valid_datetime_start': "2016-10-31 07:45:34",
            'create_count': 10,
            'coupon_type': 'discount',
            'coupon_using_count': 10,
            'coupon_value': 50,
            'valid_datetime_end': "2016-12-25 07:45:34",
            'coupon_using_user': 5
        }
        response = self.client.post('/apis/v1/coupons/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content['coupon_type'], 'discount')
        self.assertEqual(len(content['coupon_codes']), content['create_count'])

    def test_create_coupon_required(self):
        """
        创建优惠码缺少必填项
        """
        data = {
            'valid_datetime_start': "2016-10-31 07:45:34",
            'create_count': '10',
            'coupon_using_count': '10',
            'coupon_value': '50',
            'valid_datetime_end': "2016-12-25 07:45:34",
            'coupon_using_user': '5'
        }
        response = self.client.post('/apis/v1/coupons/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_coupon_in_range(self):
        """
        创建优惠码,范围异常
        """
        data = {
            'valid_datetime_start': "2016-10-31 07:45:34",
            'create_count': '-10',
            'coupon_using_count': '10',
            'coupon_type': 'discountt',
            'coupon_value': '50',
            'valid_datetime_end': "2016-12-25 07:45:34",
            'coupon_using_user': '5'
        }
        response = self.client.post('/apis/v1/coupons/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_coupon_validate(self):
        """
        创建优惠码,数据错误
        """
        data = {
            'valid_datetime_start': "2016-10-31 07:45:34",
            'create_count': '10',
            'coupon_using_count': '10',
            'coupon_type': 'discountt',
            'coupon_value': '50',
            'valid_datetime_end': "2016-12-25 07:45:34",
            'coupon_using_user': '5'
        }
        response = self.client.post('/apis/v1/coupons/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_coupon_no_body(self):
        """
        创建优惠码,无输入项
        """
        data = {}
        response = self.client.post('/apis/v1/coupons/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_coupon_by_uuid(self):
        """
        获取优惠码详情
        """
        response = self.client.get('/apis/v1/coupons/d6e7daa6a34311e6b6946451066036bd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['coupon_type'], 'reduce')
        self.assertEqual(content['coupon_code'], '8P83FEUP')
    def test_get_coupon_by_uuid(self):
        """
        获取优惠码详情
        """
        response = self.client.get('/apis/v1/coupons/d6e7daa6a34311e6b6946451066036bd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['coupon_type'], 'reduce')
        self.assertEqual(content['coupon_code'], '8P83FEUP')

    def test_get_coupon_by_uuid_validate(self):
        """
        获取优惠码详情,无效uuid
        """
        response = self.client.get('/apis/v1/coupons/d6e7daa6a34311e6b6946451066036bdd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_coupon_by_uuid_not_exist(self):
        """
        获取优惠码详情,不存在
        """
        response = self.client.get('/apis/v1/coupons/d6e7daa6a34311e6b6946451066036cd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
    def test_get_coupon_by_code(self):
        """
        获取优惠码详情
        """
        response = self.client.get('/apis/v1/coupons/8P83FEUP/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['coupon_type'], 'reduce')
        self.assertEqual(content['coupon_code'], '8P83FEUP')
    def test_get_coupon_by_code_not_exist(self):
        """
        获取优惠码详情,不存在code
        """
        response = self.client.get('/apis/v1/coupons/8P83FEAP/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    def test_bind_coupon(self):
        """
        测试绑定优惠码功能
        """
        data = {
            'user_uuid': "22",
        }
        response = self.client.post('/apis/v1/coupons/QSSASDSD/binding', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_bind_coupon_not_exist(self):
        """
        测试绑定优惠码功能
        """
        data = {
            'user_uuid': "22",
        }
        response = self.client.post('/apis/v1/coupons/QSSASDSD/binding', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_get_coupon_bindings(self):
        """
        获取用户绑定的优惠码
        """
        response = self.client.get('/apis/v1/coupons/bindings/?user_uuid=123')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_coupon_bindings_not_exist(self):
        """
        获取用户绑定的优惠码
        """
        response = self.client.get('/apis/v1/coupons/bindings/?user_uuid=123')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CouponUsageTests(APITestCase):
    """
    Test Coupon usage's API, include list and use. 
    """
    fixtures = ['fixtures/coupon.json']
        
    def test_get_coupon_usage(self):
        """
        获取优惠码使用记录
        """
        response = self.client.get('/apis/v1/coupons/usage/?coupon_code=6U8VNJ5W')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content['content']), content['count'])

    def test_get_coupon_usage_valide(self):
        """
        获取优惠码使用记录,非法uuid
        """
        response = self.client.get('/apis/v1/coupons/usage/?coupon_usage_uuid=01406842a34211e6b1d76451066036bdd')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
