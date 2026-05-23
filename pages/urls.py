"""pages/urls.py"""
from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('register/', views.register, name='register'),
]
