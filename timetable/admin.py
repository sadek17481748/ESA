"""timetable/admin.py"""
from django.contrib import admin

from .models import Timetable, TimetableSlot


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'class_group', 'is_active', 'updated_at')
    list_filter = ('school', 'is_active')


@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('timetable', 'class_group', 'subject', 'weekday', 'start_time', 'end_time', 'teacher')
