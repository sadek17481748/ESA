"""
audit/apps.py
Loads signal handlers on startup so login/logout get logged.
"""
from django.apps import AppConfig


class AuditConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'audit'

    def ready(self):
        import audit.signals  # noqa: F401
