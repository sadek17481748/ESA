"""messaging/urls.py"""
from django.urls import path

from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.messages_inbox, name='inbox'),
    path('support/', views.support_list, name='support_list'),
    path('support/new/', views.support_new, name='support_new'),
    path('support/<int:case_id>/', views.support_detail, name='support_detail'),
    path('school/new/', views.school_new, name='school_new'),
    path('school/<int:conv_id>/', views.school_detail, name='school_detail'),
    path('reports/', views.reports_list, name='reports_list'),
    path('reports/create/', views.teacher_report_create, name='report_create'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
]
