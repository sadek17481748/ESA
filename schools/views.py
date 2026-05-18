"""
schools/views.py
Read-only API for schools — scoped by role (super admin vs school admin).
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core_app.permissions import IsSuperAdmin
from .models import School
from .serializers import SchoolSerializer


class SchoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/schools/
    Super admin: all schools. School admin: own school only.
    """

    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # list/retrieve open to any authenticated user with queryset filtering
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


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — school admin got empty list (filtered wrong field)
# ---------------------------------------------------------------------------
# def get_queryset(self):
#     user = self.request.user
#     qs = School.objects.all()
#     if user.role == 'super_admin':
#         return qs
#     if user.role == 'school_admin':
#         return qs.filter(name=user.school.name)
#     return qs.none()
