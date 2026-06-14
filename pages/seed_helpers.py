"""Shared helpers for idempotent demo seeding — preserve passwords on deploy."""
from django.contrib.auth import get_user_model

User = get_user_model()

# Only these accounts get passwords reset on every Heroku boot.
PUBLIC_DEMO_USERNAMES = frozenset({'schooladmin', 'super', 'parent_demo'})

PERSONAL_PARENT_EMAIL = 'msadekhussain@outlook.com'
PERSONAL_TEACHER_EMAIL = 'msadekhussain2001@gmail.com'
PERSONAL_PARENT_PASSWORD = 'Parent2026!'
PERSONAL_TEACHER_PASSWORD = 'Teacher2026!'


def should_reset_password(username, *, created):
    if username in PUBLIC_DEMO_USERNAMES:
        return True
    return created


def upsert_user(
    username,
    *,
    email,
    role,
    password,
    school=None,
    first_name='',
    last_name='',
    email_verified=True,
    force_reset_password=None,
):
    """
    Create or update a user without wiping passwords on every deploy.
    force_reset_password: True/False overrides the default policy.
    """
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email},
    )
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.role = role
    user.school = school
    user.is_active = True
    user.email_verified = email_verified

    if force_reset_password is None:
        reset = should_reset_password(username, created=created)
    else:
        reset = force_reset_password

    if reset:
        user.set_password(password)

    user.save()
    return user, created
