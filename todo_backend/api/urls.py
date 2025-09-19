from django.urls import path
from .views import health, todos, todo_detail

urlpatterns = [
    # Health
    path('health/', health, name='Health'),

    # ToDo endpoints
    path('todos/', todos, name='todo-list-create'),
    path('todos/<int:pk>/', todo_detail, name='todo-detail'),
]
