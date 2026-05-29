"""attendance/urls.py"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AttendanceSessionViewSet

router = DefaultRouter()
router.register('sessions', AttendanceSessionViewSet, basename='attendance-session')

urlpatterns = [path('', include(router.urls))]
