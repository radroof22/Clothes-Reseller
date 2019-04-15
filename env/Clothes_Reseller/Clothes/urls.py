
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^accounts/signup/$', views.signup, name="Signup"),
    url(r'^accounts/setup/paypal/$', views.RequirePaypal, name="Paypal_require"),
    url(r'^clothes/buy/(?P<id>[0-9]+)/$', views.Confirm_Purchase, name="Purchase_Confirmation"),
    url(r'profile/$', views.Profile, name="Profile"),
    url(r'^clothes/new/$', views.NewClothing.as_view(), name="NewClothing"),
    url(r'^clothes/$', views.ListofProducts, name="List"),
    url(r'^clothes/(?P<id>[0-9]+)/$', views.ProductDetail, name="ClothingDetail"),
    url(r'^transaction/failed/', views.Payment_Failure, name="Trans_Fail"),
    url(r'clothes/shipping/confirm/(?P<id>[0-9]+)/$', views.Shipping_Confirm, name="Shipping_Confirm"),
    url(r'^transaction/success/', views.Payment_Success, name="Trans_Success"),
    url(r'^$', views.Home, name="Home")
]
