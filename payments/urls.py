"""
payments/urls.py
Parent payment pages and Stripe webhook.
"""
from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.fee_list, name='fee_list'),
    path('school/', views.school_fees, name='school_fees'),
    path('subscription/', views.subscription_page, name='subscription'),
    path('subscription/checkout/', views.subscription_checkout, name='subscription_checkout'),
    path('subscription/cancel/', views.subscription_cancel, name='subscription_cancel'),
    path('checkout/<int:fee_id>/', views.create_checkout, name='create_checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]
