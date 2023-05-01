from django.urls import path
from .views import (
    LoginView,
    VendorRegisterView,
    CustomerRegisterView,
    VendorListView,
    VendorProfileView,
    # CustomerProfileView
    VendorDetailAPIView,
    CustomerListView,
    VendorListView,
    VendorQuantityView,
    CustomerQuantityView,


    CartView,
    AddToCartView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('vendor/register', VendorRegisterView.as_view(), name='vendor-register'),
    path('customer/register', CustomerRegisterView.as_view(), name='customer-register'),
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    # path('vendor/<int:id>/profile', VendorProfileView.as_view(), name='vendor-list'),
    # path('customer/<int:id>/profile', CustomerProfileView.as_view(), name='customer-list'),
    path('vendor/profile/<str:token>', VendorProfileView.as_view(), name='vendor-profile'),
    path('vendor/detail/<int:id>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('customer/list/', CustomerListView.as_view(), name='сustomer-list'),
    path('vendor/list/', VendorListView.as_view(), name='vendor-list'),
    path('vendor/quantity/', VendorQuantityView.as_view(), name='vendor-list'),
    path('customer/quantity/', CustomerQuantityView.as_view(), name='vendor-list'),

    path('cart/<int:user_id>/', CartView.as_view(), name='cart'),
    path('cart/<int:user_id>/add/', AddToCartView.as_view(), name='add-cart'),
]