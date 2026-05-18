"""
accounts/views.py
REST endpoints for profile, registration, and super-admin user listing.
"""
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from audit.models import AuditLog
from audit.services import log_action
from core_app.permissions import IsSuperAdmin
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class MeView(APIView):
    """GET /api/accounts/me/ — return the logged-in user's profile."""

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class RegisterView(generics.CreateAPIView):
    """POST /api/accounts/register/ — public sign-up with role + school rules."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        # audit trail for new accounts
        log_action(
            user=user,
            action=AuditLog.ACTION_CREATE,
            resource='User',
            resource_id=user.pk,
            detail=f'Registered as {user.role}',
            request=self.request,
        )


class UserListView(generics.ListAPIView):
    """GET /api/accounts/users/ — super admin only, all platform users."""

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperAdmin)

    def get_queryset(self):
        return User.objects.select_related('school').order_by('username')
