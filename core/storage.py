"""Media storage — local dev; S3 when AWS bucket is configured."""
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def get_media_storage():
    if getattr(settings, 'USE_S3_MEDIA', False):
        from storages.backends.s3 import S3Storage
        return S3Storage()
    return FileSystemStorage(location=settings.MEDIA_ROOT)
