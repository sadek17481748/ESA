"""Mushaf PDF catalogue — 30 juz paras from static files."""
MUSHAF_PARA_COUNT = 30


def para_pdf_filename(para_number):
    """Return static-relative filename for a juz (1–30)."""
    if para_number < 1 or para_number > MUSHAF_PARA_COUNT:
        raise ValueError(f'Para must be 1–{MUSHAF_PARA_COUNT}')
    return f'quran/mushaf/para-{para_number:02d}.pdf'


def para_pdf_url(para_number):
    from django.templatetags.static import static
    return static(para_pdf_filename(para_number))
