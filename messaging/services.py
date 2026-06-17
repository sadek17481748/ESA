"""messaging/services.py — case numbers, conversation access, and participant labels."""
from django.db.models import Q

from academics.models import ClassEnrollment
from parents.models import StudentParentLink
from students.models import StudentProfile

from .models import SchoolConversation, SupportCase


def generate_case_number():
    prefix = 'ESA'
    last = SupportCase.objects.order_by('-pk').first()
    seq = (last.pk + 1) if last else 1
    return f'{prefix}-{seq:05d}'


def user_can_view_conversation(user, conversation):
    if conversation.created_by_id == user.pk:
        return True
    if conversation.recipient_user_id == user.pk:
        return True
    if conversation.recipient_type == SchoolConversation.RECIPIENT_SCHOOL:
        if user.role == 'school_admin' and user.school_id == conversation.school_id:
            return True
    if user.role == 'school_admin' and user.school_id == conversation.school_id:
        if conversation.created_by.role in ('parent', 'teacher'):
            return True
    return False


def conversations_for_user(user):
    school = user.school
    if not school and user.role != 'super_admin':
        return SchoolConversation.objects.none()

    if user.role == 'school_admin':
        return SchoolConversation.objects.filter(school=school).select_related(
            'created_by', 'recipient_user',
        )

    return SchoolConversation.objects.filter(
        Q(created_by=user) | Q(recipient_user=user),
        school=school,
    ).select_related('created_by', 'recipient_user')


def support_cases_for_user(user):
    if user.role == 'super_admin':
        return SupportCase.objects.select_related('opened_by').all()
    return SupportCase.objects.filter(opened_by=user)


def build_school_messaging_context(school):
    """Lookups for school admin participant labels (class, linked children)."""
    student_class = {}
    students_by_user_id = {}

    enrollments = ClassEnrollment.objects.filter(
        class_group__school=school,
    ).select_related('student', 'class_group', 'student__user')
    for enrollment in enrollments:
        student_class[enrollment.student_id] = enrollment.class_group.name
        if enrollment.student.user_id:
            students_by_user_id[enrollment.student.user_id] = enrollment.student

    for student in StudentProfile.objects.filter(school=school, is_active=True).select_related('user'):
        if student.user_id:
            students_by_user_id[student.user_id] = student

    parent_children = {}
    links = StudentParentLink.objects.filter(student__school=school).select_related(
        'student', 'parent__user',
    )
    for link in links:
        parent_children.setdefault(link.parent.user_id, []).append(link.student.full_name)

    return {
        'student_class': student_class,
        'students_by_user_id': students_by_user_id,
        'parent_children': parent_children,
    }


def participant_label(user, ctx):
    """Display name with class (students) or children in brackets (parents)."""
    if not user:
        return ''

    name = user.get_full_name().strip() or user.username

    if user.role == 'student':
        profile = ctx['students_by_user_id'].get(user.pk)
        if profile:
            class_name = ctx['student_class'].get(profile.pk, '')
            if class_name:
                return f'{profile.full_name} · {class_name}'
            return profile.full_name
        return name

    if user.role == 'parent':
        children = ctx['parent_children'].get(user.pk, [])
        if children:
            return f'{name} ({", ".join(children)})'
        return name

    return name


def conversation_participant_line(conv, ctx):
    """Single-line summary of who is in the thread (for school admin inbox)."""
    creator = participant_label(conv.created_by, ctx)
    if conv.recipient_type == SchoolConversation.RECIPIENT_SCHOOL:
        return creator
    if conv.recipient_user:
        recipient = participant_label(conv.recipient_user, ctx)
        return f'{creator} ↔ {recipient}'
    return creator


def enrich_conversations_for_admin(conversations, school):
    """Attach participant labels for school admin inbox and thread headers."""
    ctx = build_school_messaging_context(school)
    rows = []
    for conv in conversations:
        rows.append({
            'conversation': conv,
            'participant_line': conversation_participant_line(conv, ctx),
            'creator_label': participant_label(conv.created_by, ctx),
            'recipient_label': (
                participant_label(conv.recipient_user, ctx)
                if conv.recipient_user
                else ('School office' if conv.recipient_type == SchoolConversation.RECIPIENT_SCHOOL else '')
            ),
        })
    return rows, ctx


def search_students_by_name(school, query, *, limit=50):
    """School admin student lookup — name tokens, ref no., class, or portal username."""
    term = (query or '').strip()
    if not term:
        return []

    qs = StudentProfile.objects.filter(school=school, is_active=True).select_related('user')

    if term.isdigit() and len(term) >= 3:
        qs = qs.filter(
            Q(admission_number__icontains=term)
            | Q(user__username__icontains=term)
        )
    else:
        tokens = [t for t in term.split() if t]
        if len(tokens) >= 2:
            qs = qs.filter(
                Q(first_name__icontains=tokens[0], last_name__icontains=tokens[-1])
                | Q(first_name__icontains=tokens[-1], last_name__icontains=tokens[0])
                | Q(first_name__icontains=term)
                | Q(last_name__icontains=term)
            )
        else:
            qs = qs.filter(
                Q(first_name__icontains=term)
                | Q(last_name__icontains=term)
                | Q(admission_number__icontains=term)
                | Q(user__username__icontains=term)
                | Q(year_group__icontains=term)
            )

    from academics.models import ClassEnrollment

    class_matches = ClassEnrollment.objects.filter(
        class_group__school=school,
        class_group__name__icontains=term,
    ).values_list('student_id', flat=True)
    if class_matches:
        qs = qs | StudentProfile.objects.filter(pk__in=class_matches, is_active=True)

    matches = qs.distinct().order_by('last_name', 'first_name')[:limit]

    ctx = build_school_messaging_context(school)
    results = []
    for student in matches:
        class_name = ctx['student_class'].get(student.pk, '—')
        parent_names = [
            link.parent.user.get_full_name().strip() or link.parent.user.username
            for link in student.parent_links.select_related('parent__user')
        ]
        results.append({
            'student': student,
            'class_name': class_name,
            'parent_names': parent_names,
            'parent_label': ', '.join(parent_names) if parent_names else '—',
        })
    return results
