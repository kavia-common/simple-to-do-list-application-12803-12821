from django.contrib import admin
from .models import ToDoItem


@admin.register(ToDoItem)
class ToDoItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_completed", "priority", "due_date", "created_at", "updated_at")
    list_filter = ("is_completed", "priority", "due_date", "created_at")
    search_fields = ("title", "description")
    ordering = ("is_completed", "priority", "-created_at")
