# -*- coding:utf-8 -*-

from __future__ import absolute_import, unicode_literals
from rest_framework import status
from rest_framework.test import APITestCase
import json

class ReconciliationTests(APITestCase):
    """
    Test Reconciliation's API, include list, retrieve, deal
    """
    # Mock Data from database: python manage.py dumpdata module_reconciliation -a > fixtures/reconciliation.json
    fixtures = ['fixtures/reconciliation.json']


    def test_list_reconciliation(self):
        """
        Ensure list reconciliations func
        """
        response = self.client.get('/apis/v1/reconciliations/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(content), 3)
        
    def test_get_reconciliation(self):
        """
        Ensure get a reconciliation func
        """
        response = self.client.get('/apis/v1/reconciliations/01339774-a6f4-11e6-9184-6451066036bd/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['error_message'], 'miss')

    def test_get_reconciliation_not_exist(self):
        """
        Ensure get a reconciliation func
        """
        response = self.client.get('/apis/v1/reconciliations/01339774-a6f4-11e6-9184-6451066036bc/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_reconciliation_error_uuid(self):
        """
        Ensure get a reconciliation func
        """
        response = self.client.get('/apis/v1/reconciliations/01339774-a6f4-11e6-9184-6451066036bcc/')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deal_reconciliation(self):
        """
        Ensure deal a reconciliation func
        """
        data = {
                "deal_result": "done",
                "deal_status": "close"
        }
        response = self.client.post('/apis/v1/reconciliations/014e8a52a6f411e691846451066036bd/deal/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content['deal_status'], "close")

    def test_deal_reconciliation_nobody(self):
        """
        Ensure deal a reconciliation func
        """
        data = {}
        response = self.client.post('/apis/v1/reconciliations/014e8a52a6f411e691846451066036bd/deal/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deal_reconciliation_error_param(self):
        """
        Ensure deal a reconciliation func
        """
        data = {
            "deal_result": "done",
            "deal_status": "closee"
        }
        response = self.client.post('/apis/v1/reconciliations/014e8a52a6f411e691846451066036bd/deal/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deal_reconciliation_not_exist(self):
        """
        Ensure deal a reconciliation func
        """
        data = {
            "deal_result": "done",
            "deal_status": "close"
        }
        response = self.client.post('/apis/v1/reconciliations/014e8a52a6f411e691846451066036bc/deal/', data)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
