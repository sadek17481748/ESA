"""Tenant scoping helpers — every school-bound queryset should use these."""


class TenantScopedQuerySetMixin:
    """
    Filter queryset to the current user's school.
    Super admins see everything; everyone else is scoped to request.user.school.
    """

    school_field = 'school'

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.role == 'super_admin':
            return qs
        if not user.school_id:
            return qs.none()
        return qs.filter(**{self.school_field: user.school})


class TenantScopedModelMixin:
    """Model mixin — optional school FK enforcement on save for non-super users."""

    pass

# bug: filtered with school_id= instead of school= — returned empty queryset for valid users
# return qs.filter(school_id=user.school)
