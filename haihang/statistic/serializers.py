# -*- coding:utf-8 -*-
#!/usr/bin/python
from rest_framework import serializers
from statistic.models import HostStatistic
from statistic.models import HostStatisticPlus
from statistic.models import HostStatisticTest



class HostStatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = HostStatistic
        fields = '__all__'
class HostStatisticPlusSerializer(serializers.ModelSerializer):

    class Meta:
        model = HostStatisticPlus
        fields = '__all__'


class HostStatisticTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostStatisticTest
        fields = '__all__'
        

# class HostStatisticTestSerializer(serializers.Serializer):
#     created = serializers.DateTimeField()
#     host_uuid = serializers.UUIDField()
#     user_uuid = serializers.UUIDField()
#     host_starttime = serializers.DateTimeField()
#     host_status = serializers.IntegerField()
#     host_cpu = serializers.IntegerField()
#     host_mem = serializers.IntegerField()
#     host_disk = serializers.IntegerField()
#     host_net = serializers.CharField(max_length=50,default='Free')
#     run_time = serializers.IntegerField()
#     record_status = serializers.BooleanField(default=True)
#     def create(self, validated_data):
#         return Comment(**validated_data)
#     def update(selfs,instance,validated_data):
#         instance.created = validated_data.get('created',instance.created)
#         instance.host_uuid = validated_data.get('host_uuid',instance.host_uuid)
#         instance.host_starttime = validated_data.get('host_starttime',instance.host_starttime)
#         instance.user_uuid = validated_data.get('user_uuid',instance.user_uuid)
#         instance.host_status = validated_data.get('host_status',instance.host_status)
#         instance.host_cpu = validated_data.get('host_cpu',instance,host_cpu)
#         instance.host_mem = validated_data.get('host_mem',instance.host_mem)
#         instance.host_disk = validated_data.get('host_disk',instance.host_disk)
#         instance.host_net = validated_data.get('host_net',instance.host_net)
#         instance.run_time = validated_data.get('host_time',instance.host_time)
#         instance.record_status = validated_data.get('record_status',instance.record_status)
#         instance.save()
#         return instance
