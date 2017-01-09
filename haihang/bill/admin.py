

# Register your models here.
from bill.models import Bill, BillRecord,MonthAccountRecord
from django.contrib import admin

# Register your models here.

admin.site.register(Bill)
admin.site.register(BillRecord)
admin.site.register(MonthAccountRecord)
