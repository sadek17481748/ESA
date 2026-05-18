from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'resource', 'user', 'school', 'ip_address', 'created_at')
    list_filter = ('action', 'school')
    search_fields = ('resource', 'detail', 'user__username')
    readonly_fields = ('created_at',)
