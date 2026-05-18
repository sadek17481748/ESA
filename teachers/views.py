from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolAdmin, IsSchoolStaff
from .models import TeacherProfile
from .serializers import TeacherProfileSerializer


class TeacherViewSet(TenantScopedQuerySetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated, IsSchoolStaff]

    def get_queryset(self):
        return super().get_queryset().select_related('school', 'user')
