from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from audit.models import AuditLog
from audit.services import log_action
from core_app.permissions import IsSuperAdmin
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class MeView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        log_action(
            user=user,
            action=AuditLog.ACTION_CREATE,
            resource='User',
            resource_id=user.pk,
            detail=f'Registered as {user.role}',
            request=self.request,
        )


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperAdmin)

    def get_queryset(self):
        return User.objects.select_related('school').order_by('username')
