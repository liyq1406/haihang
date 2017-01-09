from django.contrib import admin
from  statistic.models import HostStatistic,HostUser
from  statistic.models import HostStatisticTest
from  statistic.models import HostStatisticPlus

admin.site.register(HostStatistic)

admin.site.register(HostStatisticPlus)

admin.site.register(HostStatisticTest)

admin.site.register(HostUser)