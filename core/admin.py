from django.contrib import admin
from .models import ActivityLog

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user_identifier', 'action', 'details')
    list_filter = ('action',)
    search_fields = ('user_identifier', 'action', 'details')
    ordering = ('-timestamp',)
