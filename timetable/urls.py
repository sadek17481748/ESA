"""timetable/urls.py"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TimetableSlotViewSet

router = DefaultRouter()
router.register('', TimetableSlotViewSet, basename='timetable')

urlpatterns = [path('', include(router.urls))]
