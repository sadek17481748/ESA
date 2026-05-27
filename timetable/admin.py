"""timetable/admin.py"""
from django.contrib import admin

from .models import TimetableSlot


@admin.register(TimetableSlot)
class TimetableSlotAdmin(admin.ModelAdmin):
    list_display = ('class_group', 'subject', 'weekday', 'start_time', 'end_time', 'teacher')
