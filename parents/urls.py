"""parents/urls.py"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ParentViewSet, StudentParentLinkViewSet

router = DefaultRouter()
router.register('links', StudentParentLinkViewSet, basename='parent-link')
router.register('', ParentViewSet, basename='parent')

urlpatterns = [path('', include(router.urls))]
