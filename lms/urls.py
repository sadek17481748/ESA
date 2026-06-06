"""lms/urls.py"""
from django.urls import path

from . import views

app_name = 'lms'

urlpatterns = [
    path('', views.lms_hub, name='hub'),
    path('subject/new/', views.lms_subject_create, name='subject_create'),
    path('subject/<int:subject_id>/track/new/', views.lms_track_create, name='track_create'),
    path('track/<int:track_id>/upload/', views.lms_material_upload, name='material_upload'),
    path('assign/', views.lms_assign, name='assign'),
    path('complete/<int:material_id>/', views.lms_mark_complete, name='mark_complete'),
    path('submit/<int:material_id>/', views.lms_submit_material, name='submit_material'),
    path('review/<int:submission_id>/', views.lms_review_submission, name='review_submission'),
]
