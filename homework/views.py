"""
homework/views.py
Assignments, student submit, teacher sign-off.
"""
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from academics.models import ClassEnrollment
from audit.services import log_action
from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolStaff, IsStudent, IsTeacher
from notifications.services import notify_user
from .models import Assignment, Submission
from .serializers import AssignmentSerializer, SubmissionSerializer
from .services import sign_off_submission


class AssignmentViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsSchoolStaff]

    def get_queryset(self):
        qs = super().get_queryset().select_related('class_group', 'subject', 'teacher')
        user = self.request.user
        if user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            qs = qs.filter(teacher=user.teacher_profile)
        return qs

    def perform_create(self, serializer):
        teacher = getattr(self.request.user, 'teacher_profile', None)
        if not teacher and self.request.user.role != 'school_admin':
            raise PermissionError('Teachers only.')
        if teacher:
            assignment = serializer.save(school=self.request.user.school, teacher=teacher)
        else:
            assignment = serializer.save(
                school=self.request.user.school,
                teacher=serializer.validated_data['teacher'],
            )


class SubmissionViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    school_field = 'assignment__school'

    def get_queryset(self):
        qs = super().get_queryset().select_related('assignment', 'student', 'student__user')
        user = self.request.user
        if user.role == 'student' and hasattr(user, 'student_profile'):
            qs = qs.filter(student=user.student_profile)
        elif user.role == 'teacher' and hasattr(user, 'teacher_profile'):
            qs = qs.filter(assignment__teacher=user.teacher_profile)
        return qs

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsTeacher])
    def submit(self, request, pk=None):
        submission = self.get_object()
        submission.body = request.data.get('body', submission.body)
        submission.status = Submission.STATUS_SUBMITTED
        submission.submitted_at = timezone.now()
        submission.save()
        return Response(SubmissionSerializer(submission).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsTeacher])
    def sign_off(self, request, pk=None):
        submission = self.get_object()
        teacher = request.user.teacher_profile
        approve = request.data.get('approve', True)
        note = request.data.get('note', '')
        try:
            sign_off_submission(
                submission=submission,
                teacher_profile=teacher,
                approve=bool(approve),
                note=note,
            )
        except (PermissionError, ValueError) as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_403_FORBIDDEN)
        log_action(
            user=request.user, action='update', resource='Submission',
            resource_id=submission.pk, request=request,
        )
        return Response(SubmissionSerializer(submission).data)
