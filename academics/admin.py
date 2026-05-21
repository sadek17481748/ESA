"""academics/admin.py"""
from django.contrib import admin

from .models import ClassEnrollment, ClassGroup, YearGroup


@admin.register(YearGroup)
class YearGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'sort_order')


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'year_group', 'teacher')


@admin.register(ClassEnrollment)
class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_group', 'enrolled_at')
