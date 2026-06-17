"""subjects/views.py"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolAdminOnly, IsSchoolAdminOrReadOnlyStaff
from .models import Subject
from .serializers import SubjectSerializer


class SubjectViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsSchoolAdminOnly()]
        return [IsAuthenticated(), IsSchoolAdminOrReadOnlyStaff()]

    def get_queryset(self):
        return super().get_queryset().select_related('school', 'lead_teacher', 'lead_teacher__user')

    def perform_create(self, serializer):
        serializer.save(school=self.request.user.school)
