"""Template context for portal navigation highlighting and messaging badge."""


def portal_nav(request):
    match = getattr(request, 'resolver_match', None)
    return {'current_portal_url': match.url_name if match else None}


def messaging_nav(request):
    if not getattr(request, 'user', None) or not request.user.is_authenticated:
        return {'unread_message_count': 0}
    from messaging.unread import unread_conversation_count
    return {'unread_message_count': unread_conversation_count(request.user)}
