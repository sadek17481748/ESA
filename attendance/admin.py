"""attendance/admin.py"""
from django.contrib import admin

from .models import AttendanceMark, AttendanceSession


class AttendanceMarkInline(admin.TabularInline):
    model = AttendanceMark
    extra = 0


@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('class_group', 'session_date', 'taken_by')
    inlines = [AttendanceMarkInline]
