"""quran/urls.py"""
from django.urls import path

from . import views

app_name = 'quran'

urlpatterns = [
    path('', views.quran_list, name='list'),
    path('new/', views.quran_create_session, name='create'),
    path('session/<int:session_id>/', views.quran_session_detail, name='session_detail'),
    path('session/<int:session_id>/annotate/', views.quran_add_annotation, name='add_annotation'),
    path('session/<int:session_id>/upload/', views.quran_upload_audio, name='upload_audio'),
    path('session/<int:session_id>/feedback/', views.quran_upload_feedback, name='upload_feedback'),
]
