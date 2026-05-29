"""
attendance/views.py
Teachers take register; marks stored per student per session.
"""
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audit.services import log_action
from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolStaff
from .models import AttendanceMark, AttendanceSession
from .serializers import AttendanceSessionSerializer, AttendanceSessionWriteSerializer


class AttendanceSessionViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = AttendanceSession.objects.all()
    permission_classes = [IsAuthenticated, IsSchoolStaff]

    def get_serializer_class(self):
        if self.action == 'create':
            return AttendanceSessionWriteSerializer
        return AttendanceSessionSerializer

    def get_queryset(self):
        qs = super().get_queryset().select_related('class_group', 'timetable_slot').prefetch_related('marks')
        class_id = self.request.query_params.get('class_group')
        if class_id:
            qs = qs.filter(class_group_id=class_id)
        return qs

    def create(self, request, *args, **kwargs):
        ser = AttendanceSessionWriteSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        marks_data = data.pop('marks')
        session = AttendanceSession.objects.create(
            school=request.user.school,
            taken_by=request.user,
            **data,
        )
        for m in marks_data:
            AttendanceMark.objects.create(session=session, **m)
        log_action(user=request.user, action='create', resource='AttendanceSession',
                   resource_id=session.pk, request=request)
        return Response(AttendanceSessionSerializer(session).data, status=status.HTTP_201_CREATED)
