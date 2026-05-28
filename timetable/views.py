"""timetable/views.py — weekly slots; filter by class_group query param."""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolAdminOnly, IsSchoolAdminOrReadOnlyStaff
from .models import TimetableSlot
from .serializers import TimetableSlotSerializer


class TimetableSlotViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = TimetableSlot.objects.all()
    serializer_class = TimetableSlotSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAuthenticated(), IsSchoolAdminOnly()]
        return [IsAuthenticated(), IsSchoolAdminOrReadOnlyStaff()]

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            'class_group', 'subject', 'teacher', 'teacher__user',
        )
        class_id = self.request.query_params.get('class_group')
        if class_id:
            qs = qs.filter(class_group_id=class_id)
        return qs

    def perform_create(self, serializer):
        data = serializer.validated_data
        if data['end_time'] <= data['start_time']:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'end_time': 'End time must be after start time.'})
        serializer.save(school=self.request.user.school)


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — end_time before start_time was allowed
# ---------------------------------------------------------------------------
# def perform_create(self, serializer):
#     serializer.save(school=self.request.user.school)
