from django.contrib import admin

from .models import QuranAnnotation, QuranSession, QuranSessionPage


class QuranAnnotationInline(admin.TabularInline):
    model = QuranAnnotation
    extra = 0


@admin.register(QuranSession)
class QuranSessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'surah_name', 'teacher', 'status', 'created_at')
    list_filter = ('status', 'school')
    inlines = [QuranAnnotationInline]


@admin.register(QuranSessionPage)
class QuranSessionPageAdmin(admin.ModelAdmin):
    list_display = ('session', 'para_number', 'page_number', 'updated_at')
    list_filter = ('para_number',)


@admin.register(QuranAnnotation)
class QuranAnnotationAdmin(admin.ModelAdmin):
    list_display = ('session', 'ayah_number', 'tag', 'timestamp_seconds', 'created_at')
    list_filter = ('tag',)
