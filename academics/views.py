"""
academics/views.py
Year groups, classes, and enrolment — school admin writes.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolAdminOnly, IsSchoolAdminOrReadOnlyStaff
from .models import ClassEnrollment, ClassGroup, YearGroup
from .serializers import ClassEnrollmentSerializer, ClassGroupSerializer, YearGroupSerializer


class YearGroupViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = YearGroup.objects.all()
    serializer_class = YearGroupSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsSchoolAdminOnly()]
        return [IsAuthenticated(), IsSchoolAdminOrReadOnlyStaff()]

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.school)
