from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'project_name', 'status', 'priority', 'assigned_to', 'created_by', 'date_created')
    list_filter = ('status', 'priority', 'date_created')
    search_fields = ('project_name', 'project_description')
    ordering = ('-date_created',)
    autocomplete_fields = ['assigned_to', 'created_by']
