"""academics/urls.py"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClassEnrollmentViewSet, ClassGroupViewSet, YearGroupViewSet

router = DefaultRouter()
router.register('year-groups', YearGroupViewSet, basename='yeargroup')
router.register('enrollments', ClassEnrollmentViewSet, basename='enrollment')
router.register('', ClassGroupViewSet, basename='classgroup')

urlpatterns = [path('', include(router.urls))]
