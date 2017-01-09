# -*- coding:utf-8 -*-
#!/usr/bin/python
from rest_framework import serializers
from price.models import Price,PriceAddRecord
class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"

class RecordPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceAddRecord
        fields = "__all__"
