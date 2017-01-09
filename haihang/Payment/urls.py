"""Payment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
# from rest_framework_swagger.views import get_swagger_view
from module_payment_account import views as accountView
from module_coupon import views as couponView
from module_payment import views as paymentView
from module_reconciliation import views as reconciliationView
from django.contrib import admin
from bill import views as bill_views
from monitor import views as mon_views
from price import views as price_views
from statistic import views as sta_view

from cms.views import login_page, logout_page
from module_payment_account.cms import list_account, create_account, \
     edit_account, list_account_record
from module_coupon.cms import list_coupon, create_coupon, download_coupon, list_coupon_record

from price.cms import list_price
from module_payment.cms import list_payment, detail_payment, \
     list_payment_record, list_payment_refund
from module_reconciliation.cms import list_reconciliation
from configure.views import ConfigureViewSet
# from django.conf import settings
# from django.conf.urls.static import static
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'bills', bill_views.BillViewSet)
router.register(r'prices', price_views.PriceViewSet)
router.register(r'statistic',sta_view.StatisticViewSet)
router.register(r'monitor',mon_views.AccountMonitorViewSet)
router.register(r'rancher_test',sta_view.StatisticTestViewSet)
router.register(r'record_price',price_views.RecordPriceViewSet)

router.register(r'account_records', accountView.AccountRecordViewSet)
router.register(r'payment_accounts', accountView.PaymentAccountViewSet)
router.register(r'account_record/user', accountView.RecordUserViewSet)
router.register(r'payment_account/user', accountView.PaymentUserViewSet)
router.register(r'coupons', couponView.CouponViewSet)

router.register(r'payments', paymentView.PaymentViewSet)
router.register(r'payment/user', paymentView.PaymentUserViewSet)

router.register(r'reconciliations', reconciliationView.ReconciliationViewSet)
router.register(r'configure', ConfigureViewSet)

# schema_view = get_swagger_view(title='Payment API')
# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url('^$', schema_view),
    url(r'^apis/v1/', include(router.urls)),
    url(r'^con_user/', sta_view.con_user),


    # session
    url(r'^cms/login/$', login_page),   
    url(r'^cms/logout/$', logout_page),

    # payment account
    url(r'^cms/account/$', list_account),
    url(r'^cms/account/create/$', create_account),
    url(r'^cms/account/(?P<pk>[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})/edit/$', edit_account),
    url(r'^cms/account/(?P<pk>[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})/record/$', list_account_record),

    # coupon
    url(r'^cms/coupon/$', list_coupon),
    url(r'^cms/coupon/create/$', create_coupon),
    url(r'^cms/coupon/download/$', download_coupon),
    url(r'^cms/coupon/(?P<pk>[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})/record/$', list_coupon_record),

    url(r'^cms/price/$', list_price),
    # payment
    url(r'^cms/payment/$', list_payment),
    url(r'^cms/payment/refund/$', list_payment_refund),
    url(r'^cms/payment/(?P<pk>[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})/detail/$', detail_payment),
    url(r'^cms/payment/(?P<pk>[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12})/record/$', list_payment_record),

    # reconciliation
    url(r'^cms/reconciliation/$', list_reconciliation),
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
