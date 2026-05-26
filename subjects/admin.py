"""subjects/admin.py"""
from django.contrib import admin

from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'track', 'school', 'lead_teacher', 'is_active')
    list_filter = ('track', 'school')
