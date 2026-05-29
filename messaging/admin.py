"""messaging/admin.py"""
from django.contrib import admin

from .models import SchoolConversation, SchoolMessage, SupportCase, SupportMessage, TeacherReport


class SupportMessageInline(admin.TabularInline):
    model = SupportMessage
    extra = 0


@admin.register(SupportCase)
class SupportCaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'subject', 'opened_by', 'status', 'updated_at')
    inlines = [SupportMessageInline]


@admin.register(SchoolConversation)
class SchoolConversationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'school', 'created_by', 'recipient_type', 'updated_at')


@admin.register(TeacherReport)
class TeacherReportAdmin(admin.ModelAdmin):
    list_display = ('subject_line', 'student', 'teacher', 'created_at')
