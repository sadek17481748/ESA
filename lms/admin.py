"""lms/admin.py"""
from django.contrib import admin

from .models import ClassTrackAssignment, CourseMaterial, CourseSubject, CourseTrack, StudentMaterialProgress


class CourseTrackInline(admin.TabularInline):
    model = CourseTrack
    extra = 0


class CourseMaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 0


@admin.register(CourseSubject)
class CourseSubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    inlines = [CourseTrackInline]


@admin.register(CourseTrack)
class CourseTrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')
    inlines = [CourseMaterialInline]


@admin.register(ClassTrackAssignment)
class ClassTrackAssignmentAdmin(admin.ModelAdmin):
    list_display = ('class_group', 'track', 'assigned_at')
