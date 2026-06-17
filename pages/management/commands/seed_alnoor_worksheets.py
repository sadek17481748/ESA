"""
Seed Al-Noor Academy LMS with worksheets from WORKSHEETS/ (local) or --dir on Heroku.

Maps files to CourseSubject tracks:
  Maths     — Cluey year-level PDFs
  English   — ISL Collective grammar / spelling / comprehension PDFs
  Islamic Studies — Sahih al-Bukhari volumes + reader excerpts

Run locally against production DB:
  DATABASE_URL=$(heroku config:get DATABASE_URL -a esa-project) python manage.py seed_alnoor_worksheets

On Heroku (after ps:copy WORKSHEETS folder):
  heroku run python manage.py seed_alnoor_worksheets --dir WORKSHEETS -a esa-project
"""
import re
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from academics.models import ClassGroup
from lms.models import ClassTrackAssignment, CourseMaterial, CourseSubject, CourseTrack
from schools.models import School

SCHOOL_NAME = 'Al-Noor Academy'

SOURCE_MATHS = 'https://go.clueylearning.com.au/en/maths-worksheets/'
SOURCE_ENGLISH = 'https://en.islcollective.com/english-esl-worksheets/search'
SOURCE_BUKHARI_BASE = (
    'https://uploads.ahlesunnatpak.com/books/Saheh%20Al-Bukhari/english/'
)

BUKHARI_URLS = {
    'sahihal-bukharivol.1-ahadith1-875.pdf': f'{SOURCE_BUKHARI_BASE}SahihAl-bukhariVol.1-Ahadith1-875.pdf',
    'sahihal-bukharivol.2-ahadith876-1772.pdf': f'{SOURCE_BUKHARI_BASE}SahihAl-bukhariVol.2-Ahadith876-1772.pdf',
    'sahihal-bukharivol.3-ahadith1773-2737.pdf': f'{SOURCE_BUKHARI_BASE}SahihAl-bukhariVol.3-Ahadith1773-2737.pdf',
}


def _human_title(filename: str) -> str:
    stem = Path(filename).stem.replace('-', ' ').replace('_', ' ')
    stem = re.sub(r'clueylearning\.com\.au-\d+', '', stem, flags=re.I)
    stem = re.sub(r'\s+', ' ', stem).strip()
    return stem[:200] or filename


def _classify(filename: str):
    """Return (subject, track, source_url, use_external_only)."""
    lower = filename.lower()

    if 'bukhari' in lower:
        vol = 'Volume 1'
        if 'vol.2' in lower or 'vol2' in lower:
            vol = 'Volume 2'
        elif 'vol.3' in lower or 'vol3' in lower:
            vol = 'Volume 3'
        url = BUKHARI_URLS.get(lower.replace(' ', ''), '')
        if not url:
            for key, val in BUKHARI_URLS.items():
                if key in lower.replace(' ', ''):
                    url = val
                    break
        return (
            'Islamic Studies',
            f'Sahih al-Bukhari — {vol}',
            url or f'{SOURCE_BUKHARI_BASE}SahihAl-bukhariVol.3-Ahadith1773-2737.pdf',
            True,
        )

    if re.match(r'^\d+\.pdf$', lower):
        num = lower.replace('.pdf', '')
        return (
            'Islamic Studies',
            'Hadith reader excerpts',
            f'{SOURCE_BUKHARI_BASE}SahihAl-bukhariVol.3-Ahadith1773-2737.pdf',
            False,
        )

    year_match = re.search(r'year[- ]?(\d+)', lower)
    if year_match or 'clueylearning' in lower or 'maths-worksheet' in lower:
        year = year_match.group(1) if year_match else '7'
        return ('Maths', f'Year {year}', SOURCE_MATHS, False)

    if any(k in lower for k in ('grammar', 'proofread', 'punctuation', 'apostrophe', 'newspaper_report')):
        return ('English', 'Grammar & writing', SOURCE_ENGLISH, False)

    if 'spelling' in lower:
        return ('English', 'Spelling', SOURCE_ENGLISH, False)

    if any(k in lower for k in ('comprehension', 'victorian', 'workhouse', 'vocabulary', 'reading')):
        return ('English', 'Reading & comprehension', SOURCE_ENGLISH, False)

    return ('English', 'General English', SOURCE_ENGLISH, False)


class Command(BaseCommand):
    help = 'Upload WORKSHEETS/ PDFs into Al-Noor LMS subjects (idempotent)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir',
            default=str(settings.BASE_DIR / 'WORKSHEETS'),
            help='Folder containing worksheet PDFs',
        )
        parser.add_argument(
            '--assign-classes',
            action='store_true',
            help='Assign year tracks to matching class groups (7A → Year 7, etc.)',
        )

    def handle(self, *args, **options):
        root = Path(options['dir'])
        if not root.is_dir():
            self.stderr.write(self.style.ERROR(f'Folder not found: {root}'))
            return

        school = School.objects.filter(name=SCHOOL_NAME).first()
        if not school:
            self.stderr.write(self.style.ERROR(f'School not found: {SCHOOL_NAME}'))
            return

        pdfs = sorted(root.glob('*.pdf'))
        if not pdfs:
            self.stderr.write(self.style.WARNING(f'No PDFs in {root}'))
            return

        created = 0
        updated = 0
        subject_cache = {}
        track_cache = {}

        for path in pdfs:
            subject_name, track_name, source_url, external_only = _classify(path.name)
            title = _human_title(path.name)

            if subject_name not in subject_cache:
                subject_cache[subject_name], _ = CourseSubject.objects.get_or_create(
                    school=school,
                    name=subject_name,
                    defaults={'description': f'{subject_name} — Al-Noor LMS'},
                )
            subject = subject_cache[subject_name]

            track_key = (subject_name, track_name)
            if track_key not in track_cache:
                track_cache[track_key], _ = CourseTrack.objects.get_or_create(
                    subject=subject,
                    name=track_name,
                    defaults={'description': f'Source: {source_url}', 'sort_order': 0},
                )
            track = track_cache[track_key]

            description = f'Source: {source_url}'
            material, was_created = CourseMaterial.objects.get_or_create(
                track=track,
                title=title,
                defaults={
                    'description': description,
                    'material_type': CourseMaterial.TYPE_WORKSHEET,
                    'sort_order': created,
                },
            )

            changed = False
            if material.description != description:
                material.description = description
                changed = True

            if external_only:
                url = BUKHARI_URLS.get(path.name.lower(), source_url)
                if material.external_url != url:
                    material.external_url = url
                    changed = True
            elif path.is_file():
                with path.open('rb') as fh:
                    material.file.save(path.name, File(fh), save=False)
                material.external_url = source_url
                changed = True

            if changed or was_created:
                material.save()
            if was_created:
                created += 1
                self.stdout.write(f'  + {subject_name} / {track_name}: {title}')
            elif changed:
                updated += 1
                self.stdout.write(f'  ~ {subject_name} / {track_name}: {title}')

        if options['assign_classes']:
            self._assign_tracks(school)

        self.stdout.write(self.style.SUCCESS(
            f'LMS worksheets: {created} created, {updated} updated ({len(pdfs)} PDFs in {root})'
        ))

    def _assign_tracks(self, school):
        """Link Year N maths tracks to class groups whose year group matches."""
        for cg in ClassGroup.objects.filter(school=school).select_related('year_group'):
            yg_name = (cg.year_group.name if cg.year_group else '') or cg.name
            year_digits = re.search(r'\d+', yg_name)
            if not year_digits:
                continue
            year_label = f'Year {year_digits.group()}'
            track = CourseTrack.objects.filter(
                subject__school=school,
                subject__name='Maths',
                name=year_label,
            ).first()
            if track:
                ClassTrackAssignment.objects.get_or_create(
                    class_group=cg,
                    track=track,
                )
            for subj in ('English', 'Islamic Studies'):
                for track in CourseTrack.objects.filter(subject__school=school, subject__name=subj):
                    ClassTrackAssignment.objects.get_or_create(class_group=cg, track=track)
