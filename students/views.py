"""
students/views.py
CRUD API for students — queryset filtered to request.user.school via mixin.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from audit.services import log_action
from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolStaff
from .models import StudentProfile
from .serializers import StudentProfileSerializer


class StudentViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    """GET/POST/PATCH /api/students/ — school staff only."""

    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsSchoolStaff]

    def get_queryset(self):
        return super().get_queryset().select_related('school', 'user')

    def perform_create(self, serializer):
        user = self.request.user
        school = user.school
        if user.role == 'super_admin':
            school = serializer.validated_data.get('school') or school
        instance = serializer.save(school=school)
        log_action(
            user=user,
            action='create',
            resource='StudentProfile',
            resource_id=instance.pk,
            request=self.request,
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        log_action(
            user=self.request.user,
            action='update',
            resource='StudentProfile',
            resource_id=instance.pk,
            request=self.request,
        )


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — teacher saw students from every school
# ---------------------------------------------------------------------------
# class StudentViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
#     def get_queryset(self):
#         return StudentProfile.objects.all()
