from django.contrib import admin

from .models import Task, Category, Subtask


class SubtaskInLine(admin.StackedInline):
    model = Subtask
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created', 'updated']
    list_filter = ['author', 'status', 'created', 'category__name']
    search_fields = ('title', 'author__first_name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    raw_id_fields = ('author',)
    ordering = ('status', 'created')
    inlines = [SubtaskInLine]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    prepopulated_fields = {'slug': ('name',)}
