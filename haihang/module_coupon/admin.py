from django.contrib import admin
from models import Coupon,CouponUser,CouponUsage
# Register your models here.
admin.site.register(Coupon)
admin.site.register(CouponUsage)
admin.site.register(CouponUser)