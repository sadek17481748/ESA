from django.urls import path

from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.fee_list, name='fee_list'),
    path('checkout/<int:fee_id>/', views.create_checkout, name='create_checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]
