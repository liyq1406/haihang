from django.contrib import admin

# Register your models here.
from module_payment_account.models import PaymentAccount,AccountRecord
admin.site.register(PaymentAccount)
admin.site.register(AccountRecord)