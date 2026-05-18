"""
core_app/mixins.py
Reusable tenant filtering for DRF viewsets.
"""


class TenantScopedQuerySetMixin:
    """
    Mixin for ModelViewSet — limits queryset to request.user.school.
    Super admins see everything; users without a school get nothing.
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
    """Placeholder for future model-level tenant helpers."""

    pass


# ---------------------------------------------------------------------------
# BUGGY CODE (commented out) — wrong lookup, queryset always empty for teachers
# ---------------------------------------------------------------------------
# def get_queryset(self):
#     qs = super().get_queryset()
#     user = self.request.user
#     if user.role == 'super_admin':
#         return qs
#     return qs.filter(school_id=user.school)
