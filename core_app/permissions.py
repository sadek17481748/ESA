"""
core_app/permissions.py
DRF permission classes — one per ESA role or staff group.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


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


class IsSchoolAdminOnly(BasePermission):
    """Write operations reserved for school admin."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'school_admin'
        )


class IsSchoolAdminOrReadOnlyStaff(BasePermission):
    """Teachers can read; school admin can write."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return request.user.role in ('school_admin', 'teacher', 'super_admin')
        return request.user.role == 'school_admin'


class IsTeacher(RoleRequired):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'teacher'


class IsStudent(BasePermission):
    """Student portal actions — submit homework, view own timetable, etc."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'student'
        )


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
