from django.contrib import admin

from .models import QuranAnnotation, QuranSession


class QuranAnnotationInline(admin.TabularInline):
    model = QuranAnnotation
    extra = 0


@admin.register(QuranSession)
class QuranSessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'surah_name', 'teacher', 'status', 'created_at')
    list_filter = ('status', 'school')
    inlines = [QuranAnnotationInline]


@admin.register(QuranAnnotation)
class QuranAnnotationAdmin(admin.ModelAdmin):
    list_display = ('session', 'ayah_number', 'tag', 'timestamp_seconds', 'created_at')
    list_filter = ('tag',)
