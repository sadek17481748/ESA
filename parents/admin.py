"""parents/admin.py"""
from django.contrib import admin

from .models import ParentProfile, StudentParentLink


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'phone', 'is_active')


@admin.register(StudentParentLink)
class StudentParentLinkAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student', 'relationship')
