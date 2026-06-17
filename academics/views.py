"""
academics/views.py
Year groups, classes, and enrolment — school admin writes.
"""
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
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


class ClassGroupViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsSchoolAdminOnly()]
        return [IsAuthenticated(), IsSchoolAdminOrReadOnlyStaff()]

    def get_queryset(self):
        return super().get_queryset().select_related('school', 'teacher', 'teacher__user', 'year_group')

    def perform_create(self, serializer):
        user = self.request.user
        school = user.school
        if user.role == 'super_admin':
            school = serializer.validated_data.get('school') or school
        serializer.save(school=school)


class ClassEnrollmentViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = ClassEnrollment.objects.all()
    serializer_class = ClassEnrollmentSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdminOnly]
    school_field = 'class_group__school'

    def get_queryset(self):
        return super().get_queryset().select_related('class_group', 'student')

    def perform_create(self, serializer):
        student = serializer.validated_data['student']
        class_group = serializer.validated_data['class_group']
        if student.school_id != class_group.school_id:
            raise ValidationError({'student': 'Student and class must be in the same school.'})
        serializer.save()
