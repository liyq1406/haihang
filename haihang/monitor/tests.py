# -*- coding:utf-8 -*-
from rest_framework import status
from rest_framework.test import APITestCase
import datetime
import json
import requests

class MonitorTest(APITestCase):
    """
    测试monitor's api
    """
    # fixtures为测试用例所用的数据，python manage.py dumpdata monitor -a > fixtures/monitor.json
    fixtures = ['fixtures/monitor.json']
    def test_add_monitor(self):
        data =  {
                "payment_accountid": "5282a444-b054-11e6-ad20-00163e006715",
                "monitor_type": 2,
                "alter_value": 700,
                "notify_strategy": 2,
                "check_interval": 3
            }
        response = self.client.post('/apis/v1/monitor/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(len(content), 7)
        self.assertEqual(content['payment_accountid'],'5282a444-b054-11e6-ad20-00163e006715')
    def test_get_monitor(self):
        data  = {
            "payment_accountid": "5282a444-b054-11e6-ad20-00163e006735"
        }
        response = self.client.post('/apis/v1/monitor/get_monitor/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(content['monitor_uuid'], 'f75ac104-b059-11e6-b91c-00163e006725')
    def test_partial_update(self):
        data  = {
                    "monitor_type": 2,
                     "alter_value": 600,
                    "notify_strategy": 2,
                    "check_interval": 3
                }
        response = self.client.patch('/apis/v1/monitor/5282a444-b054-11e6-ad20-00163e006725/',data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(content['monitor_uuid'], '87eda308-b055-11e6-956d-00163e006725')
        
    def test_request(self):
        hosts = requests.get("http://54.223.237.110:3000/v1-usage/account/1a8/hosts", timeout=10, ).json()['hosts']
        host1 = hosts[0]
        check_time = (datetime.datetime.now() - datetime.datetime.strptime(host1['t'][0], "%Y-%m-%dT%H:%M:%SZ")).seconds
        print 'check_time:', check_time
        print 'lifetime:', host1['lifetime']
        print '误差:', check_time - host1['lifetime']