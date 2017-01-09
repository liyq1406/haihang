from django.contrib import admin
from monitor.models import  AlertRecord, UserAccount, AlertLevel





admin.site.register(AlertRecord)

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('useraccount_uuid','user_uuid','payment_account_uuid')
    search_fields = ('useraccount_uuid','user_uuid','payment_account_uuid')
    list_filter = ('useraccount_uuid','user_uuid','payment_account_uuid')
admin.site.register(UserAccount,UserAccountAdmin)

admin.site.register(AlertLevel)