# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.test import APITestCase
import json


class PriceTest(APITestCase):
    """
    测试price's api
    """
    # fixtures为测试用例所用的数据，python manage.py dumpdata price -a > fixtures/price.json
    fixtures = ['fixtures/price.json']

    def test_get_prce_byuuid(self):
        response = self.client.get("/apis/v1/prices/a6642262-b537-11e6-9523-00163e006725/")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['price'], 0.015)

    def test_list(self):
        response = self.client.get("/apis/v1/prices/")
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 6)

    def test_get_price_bycondition(self):
        data = {
            "cpu": 1,
            "mem": 1024,
            "disk": 500
        }
        response = self.client.post('/apis/v1/prices/get_price_bycondition/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['price'], 0.015)
