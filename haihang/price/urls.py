# from django.conf.urls import url
# from rest_framework.urlpatterns import format_suffix_patterns
# from price import views

# urlpatterns = [
#     url(r'^users/$', views.UserList.as_view()),
#     url(r'^users/(?P<pk>[A-Fa-f0-9]{8}-([A-Fa-f0-9]{4}-){3}[A-Fa-f0-9]{12})$', views.UserDetail.as_view),
#     url(r'^test/$',views.price_test),
#     ]

# urlpatterns = format_suffix_patterns(urlpatterns)

# from django.conf.urls import url, include
# from price import views as price_views
# from rest_framework.routers import DefaultRouter
# from rest_framework.schemas import get_schema_view
# # Create a router and register our viewsets with it.

# router = DefaultRouter()
# router.register(r'prices', price_views.PriceViewSet)
# #router.register(r'users', price_views.UserViewSet)
# #schema_view = get_schema_view(title='Pastebin API')

# # The API URLs are now determined automatically by the router.
# # Additionally, we include the login URLs for the browsable API.
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# 	#url('^schema/$', schema_view),
# ]