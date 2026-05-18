"""teachers/urls.py — /api/teachers/ router."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TeacherViewSet

router = DefaultRouter()
router.register('', TeacherViewSet, basename='teacher')

urlpatterns = [
    path('', include(router.urls)),
]
