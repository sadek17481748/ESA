from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClassGroupViewSet

router = DefaultRouter()
router.register('', ClassGroupViewSet, basename='classgroup')

urlpatterns = [
    path('', include(router.urls)),
]
