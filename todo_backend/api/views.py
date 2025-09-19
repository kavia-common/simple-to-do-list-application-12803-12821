from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.renderers import JSONRenderer
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import ToDoItem
from .serializers import ToDoItemSerializer


@api_view(['GET'])
def health(request: Request) -> Response:
    """
    Simple health check endpoint.
    Returns 200 OK with a status message.
    """
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="get",
    operation_id="todo_list",
    operation_summary="List to-do items",
    operation_description="Retrieve a paginated list of to-do items. Ocean Professional: primary=#2563EB, secondary=#F59E0B.",
    responses={200: ToDoItemSerializer(many=True)},
    manual_parameters=[
        openapi.Parameter("completed", openapi.IN_QUERY, description="Filter by completion status (true/false).", type=openapi.TYPE_BOOLEAN),
        openapi.Parameter("priority", openapi.IN_QUERY, description="Filter by priority (1..5).", type=openapi.TYPE_INTEGER),
    ],
    tags=["ToDo Items"],
)
@swagger_auto_schema(
    method="post",
    operation_id="todo_create",
    operation_summary="Create a to-do item",
    operation_description="Create a new to-do item with title, description, optional due_date, and priority.",
    request_body=ToDoItemSerializer,
    responses={201: ToDoItemSerializer, 400: "Validation error"},
    tags=["ToDo Items"],
)
@api_view(["GET", "POST"])
@renderer_classes([JSONRenderer])
def todos(request: Request) -> Response:
    """
    List or create ToDo items.

    GET /api/todos/
    Query Params:
      - completed: bool (optional) filter by completion status
      - priority: int (optional) filter by priority

    Sample Response (200):
    [
      {
        "id": 1,
        "title": "Buy milk",
        "description": "2% organic",
        "is_completed": false,
        "due_date": "2025-12-31",
        "priority": 2,
        "created_at": "2025-01-01T12:00:00Z",
        "updated_at": "2025-01-01T12:00:00Z"
      }
    ]

    POST /api/todos/
    Sample Request:
    {
      "title": "Plan sprint",
      "description": "Draft backlog",
      "is_completed": false,
      "due_date": "2025-12-31",
      "priority": 3
    }

    Sample Response (201):
    {
      "id": 2,
      "title": "Plan sprint",
      "description": "Draft backlog",
      "is_completed": false,
      "due_date": "2025-12-31",
      "priority": 3,
      "created_at": "2025-01-02T09:00:00Z",
      "updated_at": "2025-01-02T09:00:00Z"
    }
    """
    if request.method == "GET":
        qs = ToDoItem.objects.all()
        completed = request.query_params.get("completed")
        priority = request.query_params.get("priority")
        if completed is not None:
            if str(completed).lower() in ("true", "1", "yes"):
                qs = qs.filter(is_completed=True)
            elif str(completed).lower() in ("false", "0", "no"):
                qs = qs.filter(is_completed=False)
        if priority is not None:
            try:
                p = int(priority)
                qs = qs.filter(priority=p)
            except ValueError:
                pass
        serializer = ToDoItemSerializer(qs, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ToDoItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response(ToDoItemSerializer(item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# PUBLIC_INTERFACE
@swagger_auto_schema(
    method="get",
    operation_id="todo_retrieve",
    operation_summary="Retrieve a to-do item",
    operation_description="Get a single to-do item by ID.",
    responses={200: ToDoItemSerializer, 404: "Not Found"},
    tags=["ToDo Items"],
)
@swagger_auto_schema(
    method="patch",
    operation_id="todo_partial_update",
    operation_summary="Update a to-do item (partial)",
    operation_description="Partially update fields of an existing to-do item by ID.",
    request_body=ToDoItemSerializer,
    responses={200: ToDoItemSerializer, 400: "Validation error", 404: "Not Found"},
    tags=["ToDo Items"],
)
@swagger_auto_schema(
    method="put",
    operation_id="todo_update",
    operation_summary="Replace a to-do item",
    operation_description="Replace all fields of an existing to-do item by ID.",
    request_body=ToDoItemSerializer,
    responses={200: ToDoItemSerializer, 400: "Validation error", 404: "Not Found"},
    tags=["ToDo Items"],
)
@swagger_auto_schema(
    method="delete",
    operation_id="todo_delete",
    operation_summary="Delete a to-do item",
    operation_description="Delete a to-do item by ID.",
    responses={204: "No Content", 404: "Not Found"},
    tags=["ToDo Items"],
)
@api_view(["GET", "PATCH", "PUT", "DELETE"])
@renderer_classes([JSONRenderer])
def todo_detail(request: Request, pk: int) -> Response:
    """
    Retrieve, update, or delete a ToDo item.

    GET /api/todos/{id}/
    Sample Response (200):
    {
      "id": 1,
      "title": "Buy milk",
      "description": "2% organic",
      "is_completed": false,
      "due_date": "2025-12-31",
      "priority": 2,
      "created_at": "2025-01-01T12:00:00Z",
      "updated_at": "2025-01-01T12:00:00Z"
    }

    PATCH /api/todos/{id}/
    Sample Request:
    { "is_completed": true }

    PUT /api/todos/{id}/
    Sample Request:
    {
      "title": "Buy milk",
      "description": "whole milk",
      "is_completed": true,
      "due_date": "2025-12-31",
      "priority": 2
    }

    DELETE /api/todos/{id}/
    Sample Response: 204 No Content
    """
    item = get_object_or_404(ToDoItem, pk=pk)

    if request.method == "GET":
        return Response(ToDoItemSerializer(item).data)

    if request.method in ("PATCH", "PUT"):
        partial = request.method == "PATCH"
        serializer = ToDoItemSerializer(item, data=request.data, partial=partial)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(ToDoItemSerializer(updated).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
