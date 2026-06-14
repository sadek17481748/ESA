from django.contrib import admin

from .models import HifzJuzSignOff


@admin.register(HifzJuzSignOff)
class HifzJuzSignOffAdmin(admin.ModelAdmin):
    list_display = ('student', 'juz_number', 'signed_off_by', 'signed_off_at', 'school')
    list_filter = ('school', 'juz_number')
    search_fields = ('student__first_name', 'student__last_name')
