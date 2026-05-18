"""Shared tenant/RBAC utilities — no models in this app."""
from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_app'
