"""
core_app/permissions.py
DRF permission classes — one per ESA role or staff group.
"""
from rest_framework.permissions import BasePermission


class RoleRequired(BasePermission):
    """Subclass sets allowed_roles on the view, or override has_permission."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        allowed = getattr(view, 'allowed_roles', None)
        if not allowed:
            return True
        return request.user.role in allowed


class IsSuperAdmin(RoleRequired):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'super_admin'


class IsSchoolAdmin(RoleRequired):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'school_admin'


class IsTeacher(RoleRequired):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'teacher'


class IsParent(RoleRequired):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'parent'


class IsSchoolStaff(RoleRequired):
    """School admin, teacher, or super admin — anyone who works inside a tenant."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ('school_admin', 'teacher', 'super_admin')


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — checked Django is_staff, not ESA school_admin role
# ---------------------------------------------------------------------------
# class IsSchoolAdmin(RoleRequired):
#     def has_permission(self, request, view):
#         return super().has_permission(request, view) and request.user.is_staff
