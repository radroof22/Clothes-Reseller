"""Zip_Clothing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Post-Transaction
    path("transaction/off-notification/<int:trans_id>/", views.Off_Notifications, name="Off-Notifications"),
    path("transaction/receive-conf/<int:trans_id>/", views.Confirm_Receive, name="Conf-Receive"),
    path("transaction/shipping-conf/<int:trans_id>/", views.Confirm_Shipping, name="Conf-Shipping"),
    path("transaction/claim-cash/<int:trans_id>/", views.Claim_Cash, name="Claim-Cash"),
    # Payments
    path("charge", views.Charge, name="Charge"), 
    # 
    path("confirm_shipping_address", views.Shipping_Address, name="conf_ship_address"),
    # Products
    path("products/create/", views.Create_Product, name="Create_Product"),
    path("products/list/", views.Product_List, name="Product_List"),
    path("product/detail/<int:prod_id>/", views.Detail_Product, name="Detail_Product"),
    # Account
    path("accounts/sign-up/", views.Sign_Up, name="Sign_Up"),
    path("accounts/login/", views.Login, name='Login'),
    path("accounts/logout/", views.Logout, name='Logout'),
    path("profile/", views.Profile, name="Profile"),
    # Home
    path('', views.Home, name="Home")
    
]
