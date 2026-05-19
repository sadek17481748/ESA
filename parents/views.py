"""
parents/views.py
School admin manages parent accounts and links children.
"""
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from audit.services import log_action
from core_app.mixins import TenantScopedQuerySetMixin
from core_app.permissions import IsSchoolAdminOnly, IsSchoolAdminOrReadOnlyStaff
from .models import ParentProfile, StudentParentLink
from .serializers import (
    ParentCreateSerializer, ParentProfileSerializer, StudentParentLinkSerializer,
)

User = get_user_model()


class ParentViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy', 'register'):
            return [IsAuthenticated(), IsSchoolAdminOnly()]
        return [IsAuthenticated(), IsSchoolAdminOrReadOnlyStaff()]

    def get_queryset(self):
        return super().get_queryset().select_related('school', 'user')

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Create User (parent role) + ParentProfile in one step."""
        ser = ParentCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        if User.objects.filter(username=data['username']).exists():
            return Response({'username': 'Already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role='parent',
            school=request.user.school,
        )
        profile = ParentProfile.objects.create(
            school=request.user.school,
            user=user,
            phone=data.get('phone', ''),
        )
        log_action(user=request.user, action='create', resource='ParentProfile',
                   resource_id=profile.pk, request=request)
        return Response(ParentProfileSerializer(profile).data, status=status.HTTP_201_CREATED)


class StudentParentLinkViewSet(TenantScopedQuerySetMixin, viewsets.ModelViewSet):
    queryset = StudentParentLink.objects.all()
    serializer_class = StudentParentLinkSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdminOnly]
    school_field = 'parent__school'

    def get_queryset(self):
        return super().get_queryset().select_related('parent', 'student', 'parent__user')

    def perform_create(self, serializer):
        parent = serializer.validated_data['parent']
        student = serializer.validated_data['student']
        if parent.school_id != self.request.user.school_id:
            raise PermissionError('Parent must belong to your school.')
        if student.school_id != self.request.user.school_id:
            raise PermissionError('Student must belong to your school.')
        serializer.save()


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — parent register saved user without school FK
# ---------------------------------------------------------------------------
# user = User.objects.create_user(
#     username=data['username'], email=data['email'], password=data['password'], role='parent',
# )

# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — linked parent to student from another tenant
# ---------------------------------------------------------------------------
# def perform_create(self, serializer):
#     serializer.save()
