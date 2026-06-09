"""
quran/services.py
Ayah text lookup and session helpers.
"""
from django.utils import timezone

from notifications.services import notify_user

from .models import QuranAnnotation, QuranSession

# Sample ayah text for demo sessions (surah number → ayah number → text)
AYAH_SAMPLES = {
    1: {
        1: 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ',
        2: 'الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ',
        3: 'الرَّحْمَٰنِ الرَّحِيمِ',
        4: 'مَالِكِ يَوْمِ الدِّينِ',
        5: 'إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ',
        6: 'اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ',
        7: 'صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ',
    },
    112: {
        1: 'قُلْ هُوَ اللَّهُ أَحَدٌ',
        2: 'اللَّهُ الصَّمَدُ',
        3: 'لَمْ يَلِدْ وَلَمْ يُولَدْ',
        4: 'وَلَمْ يَكُنْ لَهُ كُفُوًا أَحَدٌ',
    },
}

SURAH_NAMES = {
    1: 'Al-Fatiha',
    112: 'Al-Ikhlas',
}


def build_ayah_text(surah_number, ayah_start, ayah_end):
    """Return concatenated ayah text for the given range."""
    surah = AYAH_SAMPLES.get(surah_number, {})
    lines = []
    for n in range(ayah_start, ayah_end + 1):
        text = surah.get(n)
        if text:
            lines.append(f'{n}. {text}')
    if not lines:
        return f'Surah {surah_number}, ayah {ayah_start}–{ayah_end} (text placeholder)'
    return '\n'.join(lines)


def mark_session_reviewed(session, teacher_profile, notes=''):
    if session.teacher_id != teacher_profile.id:
        raise PermissionError('Only the session teacher can mark this reviewed.')
    session.status = QuranSession.STATUS_REVIEWED
    session.teacher_notes = notes
    session.reviewed_at = timezone.now()
    session.save(update_fields=['status', 'teacher_notes', 'reviewed_at'])
    if session.student.user_id:
        notify_user(
            user=session.student.user,
            school=session.school,
            notification_type='quran',
            title='Recitation reviewed',
            message=f'{session.surah_name}: teacher feedback is ready.',
            link_path=f'/quran/session/{session.pk}/',
        )
    return session


def add_annotation(*, session, teacher_profile, ayah_number, tag, timestamp_seconds, comment=''):
    if session.teacher_id != teacher_profile.id:
        raise PermissionError('Only the session teacher can add annotations.')
    return QuranAnnotation.objects.create(
        session=session,
        ayah_number=ayah_number,
        tag=tag,
        timestamp_seconds=timestamp_seconds,
        comment=comment,
        created_by=teacher_profile,
    )
