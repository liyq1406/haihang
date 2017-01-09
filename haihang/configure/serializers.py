# -*- coding:utf-8 -*-

from configure.models import Configure
from rest_framework import serializers

class ConfigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configure
        fields = "__all__"
