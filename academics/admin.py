from django.contrib import admin

from .models import ClassGroup


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'year_group', 'teacher', 'created_at')
    list_filter = ('school', 'year_group')
    search_fields = ('name',)
