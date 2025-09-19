from rest_framework import serializers
from .models import ToDoItem


# PUBLIC_INTERFACE
class ToDoItemSerializer(serializers.ModelSerializer):
    """Serializer for ToDoItem with validation and readable date formats."""

    class Meta:
        model = ToDoItem
        fields = [
            "id",
            "title",
            "description",
            "is_completed",
            "due_date",
            "priority",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_priority(self, value: int) -> int:
        """
        Ensure priority is between 1 and 5 inclusive.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Priority must be between 1 (highest) and 5 (lowest).")
        return value
