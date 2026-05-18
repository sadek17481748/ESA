from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core_app.permissions import IsSuperAdmin
from .models import School
from .serializers import SchoolSerializer


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Super admin: all schools.
    School admin: own school only.
    """
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsSuperAdmin()]

    def get_queryset(self):
        user = self.request.user
        qs = School.objects.all()
        if user.role == 'super_admin':
            return qs
        if user.role == 'school_admin' and user.school_id:
            return qs.filter(pk=user.school_id)
        return qs.none()
