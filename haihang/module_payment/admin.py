from django.contrib import admin
from models import Payment,PaymentRecord,PaymentRefund
# Register your models here.
admin.site.register(Payment)
admin.site.register(PaymentRecord)
admin.site.register(PaymentRefund)