from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model providing created_at and updated_at timestamps.
    """
    created_at = models.DateTimeField(auto_now_add=True, help_text="When the record was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="When the record was last updated.")

    class Meta:
        abstract = True


class ToDoItem(TimeStampedModel):
    """
    To-do item representing a task in the system.
    """
    title = models.CharField(max_length=255, help_text="Short title for the task.")
    description = models.TextField(blank=True, default="", help_text="Detailed description of the task.")
    is_completed = models.BooleanField(default=False, help_text="Whether the task is completed.")
    due_date = models.DateField(null=True, blank=True, help_text="Optional due date for the task.")
    priority = models.PositiveSmallIntegerField(
        default=3,
        help_text="Task priority where 1 is highest and 5 is lowest. Default is 3."
    )

    class Meta:
        ordering = ["is_completed", "priority", "-created_at"]
        indexes = [
            models.Index(fields=["is_completed"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({'done' if self.is_completed else 'open'})"
