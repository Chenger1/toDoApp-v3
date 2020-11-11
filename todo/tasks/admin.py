from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created', 'updated']
    list_filter = ['author', 'status', 'created']
    search_fields = ('title', 'author__first_name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    raw_id_fields = ('author',)
    ordering = ('status', 'created')
