from django.contrib import admin

from .models import TeacherProfile


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'subject', 'employee_code', 'is_active')
    list_filter = ('school', 'is_active')
    search_fields = ('user__username', 'subject', 'employee_code')
