"""DRF permission classes mapped to ESA roles."""

from rest_framework.permissions import BasePermission


class RoleRequired(BasePermission):
    """Base — set allowed_roles on the view."""

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

# bug: IsSchoolAdmin used is_staff instead of role — any staff user passed
# return request.user.is_staff


class IsTeacher(RoleRequired):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'teacher'


class IsParent(RoleRequired):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == 'parent'


class IsSchoolStaff(RoleRequired):
    """School admin or teacher — both work inside one tenant."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ('school_admin', 'teacher', 'super_admin')
