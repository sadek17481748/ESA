from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolStaff
from .models import ClassGroup
from .serializers import ClassGroupSerializer


class ClassGroupViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer
    permission_classes = [IsAuthenticated, IsSchoolStaff]

    def get_queryset(self):
        return super().get_queryset().select_related('school', 'teacher', 'teacher__user')

    def perform_create(self, serializer):
        user = self.request.user
        school = user.school
        if user.role == 'super_admin':
            school = serializer.validated_data.get('school') or school
        serializer.save(school=school)
