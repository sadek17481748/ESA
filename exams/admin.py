from django.contrib import admin

from .models import Exam, ExamAnswer, ExamQuestion, ExamResult


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 0


class ExamResultInline(admin.TabularInline):
    model = ExamResult
    extra = 0
    readonly_fields = ('auto_score', 'manual_score', 'final_score', 'status')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_group', 'teacher', 'exam_date', 'status')
    list_filter = ('status', 'school')
    inlines = [ExamQuestionInline, ExamResultInline]


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'final_score', 'status', 'signed_off_at')
    list_filter = ('status',)
