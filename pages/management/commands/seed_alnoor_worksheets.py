"""
Seed Al-Noor Academy LMS with worksheets from WORKSHEETS/ (local) or --dir on Heroku.

Maps files to CourseSubject tracks:
  Maths     — Cluey year-level PDFs
  English   — ISL Collective grammar / spelling / comprehension PDFs
  Islamic Studies — Sahih al-Bukhari volumes + reader excerpts

Run locally against production DB:
  DATABASE_URL=$(heroku config:get DATABASE_URL -a esa-project) python manage.py seed_alnoor_worksheets

On Heroku (manifest + Bukhari PDF download; maths/English link to sources):
  heroku run python manage.py seed_alnoor_worksheets --assign-classes -a esa-project
"""
import re
import urllib.request
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
    'SahihAl-bukhariVol.1-Ahadith1-875.pdf': f'{SOURCE_BUKHARI_BASE}SahihAl-bukhariVol.1-Ahadith1-875.pdf',
    'SahihAl-bukhariVol.2-Ahadith876-1772.pdf': f'{SOURCE_BUKHARI_BASE}SahihAl-bukhariVol.2-Ahadith876-1772.pdf',
    'SahihAl-bukhariVol.3-Ahadith1773-2737.pdf': f'{SOURCE_BUKHARI_BASE}SahihAl-bukhariVol.3-Ahadith1773-2737.pdf',
}

WORKSHEET_MANIFEST = (
    '11.pdf', '14.pdf', '17.pdf', '2.pdf', '5.pdf', '8.pdf',
    'SahihAl-bukhariVol.1-Ahadith1-875.pdf',
    'SahihAl-bukhariVol.2-Ahadith876-1772.pdf',
    'SahihAl-bukhariVol.3-Ahadith1773-2737.pdf',
    'Year-10-Algebra-Maths-Worksheet-Add-Subtract-Polynomials-clueylearning.com.au-1300182000.pdf',
    'Year-10-Algebra-Maths-Worksheet-Multiply-Polynomials-clueylearning.com.au-1300182000.pdf',
    'Year-2-Addition-Maths-Worksheet-Maths-Riddles-clueylearning.com.au-1300182000.pdf',
    'Year-2-Maths-Worksheet-Place-the-numbers-in-order-clueylearning.com.au-1300182000.pdf',
    'Year-3-Addition-Maths-Worksheet-Adding-2-digit-and-3-digit-numbers-clueylearning.com.au-1300182000.pdf',
    'Year-3-Addition-Maths-Worksheet-Adding-two-2-digit-numbers-clueylearning.com.au-1300182000.pdf',
    'Year-3-Multiplication-Maths-Worksheet-clueylearning.com.au-1300182000.pdf',
    'Year-7-Addition-Maths-Worksheet-Adding-Negatives-clueylearning.com.au-1300182000.pdf',
    'Year-7-Division-Maths-Worksheet-Short-Division-clueylearning.com.au-1300182000.pdf',
    'Year-8-Algebra-Maths-Worksheet-Expanding-Brackets-clueylearning.com.au-1300182000.pdf',
    'Year-8-Geometry-Maths-Worksheet-Graph-Linear-Equations-clueylearning.com.au-1300182000.pdf',
    'Year-8-Measurement-Maths-Worksheet-Area-Circle-clueylearning.com.au-1300182000.pdf',
    'Year-9-Algebra-Maths-Worksheet-Simultaneous-Equations-Substitutions-clueylearning.com.au-1300182000.pdf',
    'Year-9-Geometry-Maths-Worksheet-Trigonometry-Finding-The-Unknown-Sides-Of-Right-Triangles-clueylearning.com.au-1300182000.pdf',
    'Year-9-Measurement-Maths-Worksheet-Surface-Area-Volume-Cylinder-clueylearning.com.au-1300182000.pdf',
    'Z0ZAQ1-Year-2-Addition-Maths-Worksheet-Greater-than-less-than-clueylearning.com.au-1300182000.pdf',
    'common_spelling_errors_worksheet_1.pdf',
    'common_spelling_errors_worksheet_2.pdf',
    'comprehension_questions_victorian_workhouse.pdf',
    'hpKqhM-comprehension_questions_victorian_workhouse.pdf',
    'living_in_a_victorian_workhouse_vocabulary___sheet_1.pdf',
    'living_in_a_victorian_workhouse_vocabulary___sheet_3.pdf',
    'living_in_the_victorian_workhouse_reading_comprehension___text.pdf',
    'newspaper_report_writing_dice_activity.pdf',
    'plogging_proofreading_lower_ability_apostrophes_worksheet.pdf',
    'plogging_proofreading_middle_ability_worksheet.pdf',
    'spelling_and_punctuation_mixed_apostrophe_worksheet.pdf',
    'worksheets-grammar.pdf',
)


def _human_title(filename: str) -> str:
    stem = Path(filename).stem.replace('-', ' ').replace('_', ' ')
    stem = re.sub(r'clueylearning\.com\.au-\d+', '', stem, flags=re.I)
    stem = re.sub(r'\s+', ' ', stem).strip()
    return stem[:200] or filename


def _bukhari_pdf_url(filename: str) -> str:
    key = filename.lower().replace(' ', '')
    for manifest_key, url in BUKHARI_URLS.items():
        if manifest_key.lower().replace(' ', '') in key or key in manifest_key.lower():
            return url
    return BUKHARI_URLS['sahihal-bukhariVol.3-Ahadith1773-2737.pdf']


def _classify(filename: str):
    """Return (subject, track, source_url, use_external_only)."""
    lower = filename.lower()

    if 'bukhari' in lower:
        vol = 'Volume 1'
        if 'vol.2' in lower or 'vol2' in lower:
            vol = 'Volume 2'
        elif 'vol.3' in lower or 'vol3' in lower:
            vol = 'Volume 3'
        url = _bukhari_pdf_url(lower)
        return (
            'Islamic Studies',
            f'Sahih al-Bukhari — {vol}',
            url,
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
        school = School.objects.filter(name=SCHOOL_NAME).first()
        if not school:
            self.stderr.write(self.style.ERROR(f'School not found: {SCHOOL_NAME}'))
            return

        if root.is_dir():
            filenames = sorted(p.name for p in root.glob('*.pdf'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Folder not found ({root}) — using built-in manifest ({len(WORKSHEET_MANIFEST)} worksheets)'
            ))
            filenames = list(WORKSHEET_MANIFEST)

        if not filenames:
            self.stderr.write(self.style.WARNING('No worksheets to seed'))
            return

        created = 0
        updated = 0
        subject_cache = {}
        track_cache = {}

        for name in filenames:
            path = root / name if root.is_dir() else None
            subject_name, track_name, source_url, external_only = _classify(name)
            title = _human_title(name)

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
                url = _bukhari_pdf_url(name)
                if material.external_url != url:
                    material.external_url = url
                    changed = True
                if not material.file and url:
                    try:
                        tmp = settings.MEDIA_ROOT / 'lms' / 'materials' / name
                        tmp.parent.mkdir(parents=True, exist_ok=True)
                        urllib.request.urlretrieve(url, tmp)
                        with tmp.open('rb') as fh:
                            material.file.save(name, File(fh), save=False)
                        changed = True
                    except OSError:
                        pass
            elif path and path.is_file():
                with path.open('rb') as fh:
                    material.file.save(name, File(fh), save=False)
                material.external_url = source_url
                changed = True
            else:
                if material.external_url != source_url:
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
            f'LMS worksheets: {created} created, {updated} updated ({len(filenames)} worksheets)'
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
