from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from audit.services import log_action
from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolStaff
from .models import StudentProfile
from .serializers import StudentProfileSerializer


class StudentViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
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


# bug: get_queryset returned StudentProfile.objects.all() with no school filter
# return StudentProfile.objects.all()
