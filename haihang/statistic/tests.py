# -*- coding:utf-8 -*-

from rest_framework import status
from rest_framework.test import APITestCase
import json

class StatisticTest(APITestCase):
    """
    # 测试statistic's api
    """
    # fixtures为测试用例所用的数据，python manage.py dumpdata statistic -a > fixtures/statistic.json
    fixtures = ['fixtures/statistic.json']
    def test_gain_statistic_byid(self):
        data =  {
            "host_uuid": "11c36ca8-b53c-11e6-889c-00163e006725"
            }
        response = self.client.post('/apis/v1/statistic/gain_statistic_byid/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(content['user_uuid'],'11c0d358-b53c-11e6-889c-00163e006725')
