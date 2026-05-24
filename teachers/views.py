"""
teachers/views.py
Teachers — school admin can add/edit; staff can list.
"""
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audit.services import log_action
from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolAdminOnly, IsSchoolAdminOrReadOnlyStaff
from .models import TeacherProfile
from .serializers import TeacherCreateSerializer, TeacherProfileSerializer

User = get_user_model()


class TeacherViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy', 'register'):
            return [IsAuthenticated(), IsSchoolAdminOnly()]
        return [IsAuthenticated(), IsSchoolAdminOrReadOnlyStaff()]

    def get_queryset(self):
        return super().get_queryset().select_related('school', 'user')

    @action(detail=False, methods=['post'])
    def register(self, request):
        ser = TeacherCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        if User.objects.filter(username=data['username']).exists():
            return Response({'username': 'Already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role='teacher',
            school=request.user.school,
        )
        profile = TeacherProfile.objects.create(
            school=request.user.school,
            user=user,
            subject=data.get('subject', ''),
            employee_code=data.get('employee_code', ''),
        )
        log_action(user=request.user, action='create', resource='TeacherProfile',
                   resource_id=profile.pk, request=request)
        return Response(TeacherProfileSerializer(profile).data, status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — teacher user created without school FK
# ---------------------------------------------------------------------------
# user = User.objects.create_user(
#     username=data['username'], email=data['email'], password=data['password'], role='teacher',
# )
