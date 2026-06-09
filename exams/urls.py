"""exams/urls.py"""
from django.urls import path

from . import views

app_name = 'exams'

urlpatterns = [
    path('', views.exams_list, name='list'),
    path('new/', views.exam_create, name='create'),
    path('<int:exam_id>/', views.exam_detail, name='detail'),
    path('<int:exam_id>/question/', views.exam_add_question, name='add_question'),
    path('<int:exam_id>/publish/', views.exam_publish, name='publish'),
    path('<int:exam_id>/mark/', views.exam_mark_written, name='mark_written'),
    path('<int:exam_id>/finalise/', views.exam_finalise, name='finalise'),
]
