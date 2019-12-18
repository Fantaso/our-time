from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'description',
        'deadline', 'priority', 'is_done',
        'created_at', 'updated_at',
    )
    list_filter = ('created_at', 'updated_at')
