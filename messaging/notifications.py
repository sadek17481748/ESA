"""Email alerts for school messages and support tickets."""
from core_app.email_service import platform_inbox, send_platform_email, send_user_email

from .unread import conversation_recipients_excluding_sender


def notify_school_message_recipients(message):
    """Email participants and the platform inbox when a school message is sent."""
    conv = message.conversation
    recipients = conversation_recipients_excluding_sender(conv, message.sender)
    sender_name = message.sender.get_full_name() or message.sender.username
    subject = f'New message: {conv.subject}'
    preview = message.body[:500]

    _notify_platform_school_message(conv, message, sender_name, preview)

    for user in recipients:
        if not getattr(user, 'notify_on_messages', True):
            continue
        if not user.email:
            continue
        body = (
            f'Salam {user.get_full_name() or user.username},\n\n'
            f'{sender_name} wrote in "{conv.subject}":\n\n'
            f'{preview}\n\n'
            f'Log in to ESA to read and reply.\n'
        )
        send_user_email(subject, body, [user.email])


def _notify_platform_school_message(conv, message, sender_name, preview):
    """Copy school / parent / teacher messages to the platform Gmail inbox."""
    school = conv.school
    recipient_label = conv.get_recipient_type_display()
    body = (
        f'A new school message was sent on ESA.\n\n'
        f'School: {school.name}\n'
        f'Thread: {conv.subject}\n'
        f'Recipient type: {recipient_label}\n'
        f'From: {sender_name} ({message.sender.role})\n'
        f'Email: {message.sender.email or "—"}\n\n'
        f'Message:\n{preview}\n\n'
        f'Platform inbox: {platform_inbox()}\n'
    )
    send_platform_email(
        f'[ESA] School message — {school.name} — {conv.subject}',
        body,
        reply_to=message.sender.email or None,
    )


def notify_platform_support_message(support_message):
    """Email platform inbox when a support ticket message is posted."""
    case = support_message.case
    sender = support_message.sender
    sender_name = sender.get_full_name() or sender.username
    body = (
        f'Support ticket activity on ESA.\n\n'
        f'Case: {case.case_number} — {case.subject}\n'
        f'Status: {case.get_status_display()}\n'
        f'From: {sender_name} ({sender.role})\n'
        f'Email: {sender.email or "—"}\n'
        f'Staff reply: {"yes" if support_message.is_staff_reply else "no"}\n\n'
        f'Message:\n{support_message.body[:1000]}\n'
    )
    send_platform_email(
        f'[ESA] Support — {case.case_number} — {case.subject}',
        body,
        reply_to=sender.email or None,
    )


def notify_platform_school_registration(school, admin_user):
    """Email platform inbox when a new school registers."""
    body = (
        f'A new school registered on ESA.\n\n'
        f'School: {school.name}\n'
        f'Contact email: {school.contact_email or "—"}\n'
        f'Admin: {admin_user.get_full_name() or admin_user.username}\n'
        f'Admin email: {admin_user.email or "—"}\n'
        f'Plan: {school.get_subscription_tier_display()}\n'
    )
    send_platform_email(
        f'[ESA] New school registration — {school.name}',
        body,
        reply_to=admin_user.email or school.contact_email or None,
    )
