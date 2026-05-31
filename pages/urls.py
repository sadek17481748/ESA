"""pages/urls.py — portal routes for dashboards and feature placeholders."""
from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/school/', views.register_school, name='register_school'),
    path('dashboard/', views.dashboard_router, name='dashboard'),
    path('dashboard/parent/', views.dashboard_parent, name='dashboard_parent'),
    path('dashboard/teacher/', views.dashboard_teacher, name='dashboard_teacher'),
    path('dashboard/student/', views.dashboard_student, name='dashboard_student'),
    path('dashboard/school-admin/', views.dashboard_school_admin, name='dashboard_school_admin'),
    path('dashboard/super-admin/', views.dashboard_super_admin, name='dashboard_super_admin'),
    path('attendance/', views.page_attendance, name='attendance'),
    path('behaviour/', views.page_behaviour, name='behaviour'),
    path('exams/', views.page_exams, name='exams'),
    path('hifz/', views.page_hifz, name='hifz'),
    path('messages/', views.page_messages, name='messages'),
    path('payments-info/', views.page_payments_info, name='payments_info'),
    path('quran/', views.page_quran, name='quran'),
    path('subscription/', views.page_subscription, name='subscription'),
    path('school-admin/teachers/', views.school_admin_teachers, name='school_admin_teachers'),
    path('school-admin/teachers/add/', views.school_admin_add_teacher, name='school_admin_add_teacher'),
    path('timetable/', views.page_timetable, name='timetable'),
    path('timetable/save/', views.timetable_save, name='timetable_save'),
    path('worksheets/', views.page_worksheets, name='worksheets'),
    path('analytics/', views.page_analytics, name='analytics'),
]
