"""Mark conversations read and count unread threads."""
from django.db.models import Max, Q
from django.utils import timezone

from .models import ConversationReadState, SchoolConversation, SchoolMessage


def conversation_recipients_excluding_sender(conversation, sender):
    """Users who should be notified about a new message."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    recipients = []
    if conversation.created_by_id != sender.pk:
        recipients.append(conversation.created_by)
    if conversation.recipient_user_id and conversation.recipient_user_id != sender.pk:
        recipients.append(conversation.recipient_user)
    if conversation.recipient_type == SchoolConversation.RECIPIENT_SCHOOL:
        admins = User.objects.filter(
            school=conversation.school,
            role='school_admin',
            is_active=True,
        ).exclude(pk=sender.pk)
        recipients.extend(list(admins))
    return recipients


def mark_conversation_read(user, conversation):
    """Update read state when user opens a thread."""
    ConversationReadState.objects.update_or_create(
        user=user,
        conversation=conversation,
        defaults={'last_read_at': timezone.now()},
    )


def unread_conversation_count(user):
    """Threads with messages newer than the user's last read (or never opened)."""
    if not user.is_authenticated or user.role == 'super_admin':
        return 0

    school = user.school
    if not school:
        return 0

    if user.role == 'school_admin':
        convs = SchoolConversation.objects.filter(school=school)
    else:
        convs = SchoolConversation.objects.filter(
            Q(created_by=user) | Q(recipient_user=user),
            school=school,
        )

    read_map = {
        rs.conversation_id: rs.last_read_at
        for rs in ConversationReadState.objects.filter(user=user, conversation__in=convs)
    }
    latest = (
        SchoolMessage.objects.filter(conversation__in=convs)
        .values('conversation_id')
        .annotate(latest_at=Max('created_at'))
    )
    latest_map = {row['conversation_id']: row['latest_at'] for row in latest}

    unread = 0
    for conv in convs:
        last_msg_at = latest_map.get(conv.pk)
        if not last_msg_at:
            continue
        last_read = read_map.get(conv.pk)
        if not last_read or last_msg_at > last_read:
            unread += 1
    return unread
