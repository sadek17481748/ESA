"""pages/urls.py"""
from django.urls import path
from . import views

app_name = 'pages'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard_router, name='dashboard'),
    path('dashboard/parent/', views.dashboard_parent, name='dashboard_parent'),
    path('dashboard/teacher/', views.dashboard_teacher, name='dashboard_teacher'),
    path('dashboard/student/', views.dashboard_student, name='dashboard_student'),
    path('dashboard/school-admin/', views.dashboard_school_admin, name='dashboard_school_admin'),
    path('dashboard/super-admin/', views.dashboard_super_admin, name='dashboard_super_admin'),
]
