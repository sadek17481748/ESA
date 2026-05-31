"""Template context for portal navigation highlighting."""


def portal_nav(request):
    match = getattr(request, 'resolver_match', None)
    return {'current_portal_url': match.url_name if match else None}
