"""
pages/portal.py
Shared layout context — school branding and role sidebar for portal pages.
"""

ROLE_SIDEBAR = {
    'super_admin': 'pages/includes/sidebar_super_admin.html',
    'school_admin': 'pages/includes/sidebar_school_admin.html',
    'teacher': 'pages/includes/sidebar_teacher.html',
    'student': 'pages/includes/sidebar_student.html',
    'parent': 'pages/includes/sidebar_parent.html',
}


def build_portal_context(request, page_title, page_meta=''):
    """Context for dashboard and feature pages inside the app shell."""
    user = request.user
    school = user.school if user.is_authenticated and user.school_id else None
    return {
        'page_title': page_title,
        'page_meta': page_meta,
        'sidebar_template': ROLE_SIDEBAR.get(user.role, ROLE_SIDEBAR['parent']),
        'school_name': school.name if school else '',
        'school_tier': school.get_subscription_tier_display() if school else '',
        'user_display': user.get_full_name() or user.username,
        'user_role': user.get_role_display() if user.is_authenticated else '',
    }
