from django.contrib import admin

from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'school', 'year_group', 'admission_number', 'is_active')
    list_filter = ('school', 'year_group', 'is_active')
    search_fields = ('first_name', 'last_name', 'admission_number')
