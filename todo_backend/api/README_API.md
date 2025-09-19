To-Do Backend API (Ocean Professional)

Base URL:
- /api/

Endpoints:
- GET /api/health/ — Health check.
- GET /api/todos/ — List to-do items. Query params: completed (bool), priority (int 1..5)
- POST /api/todos/ — Create a to-do item.
- GET /api/todos/{id}/ — Retrieve a to-do item.
- PATCH /api/todos/{id}/ — Partially update a to-do item.
- PUT /api/todos/{id}/ — Replace a to-do item.
- DELETE /api/todos/{id}/ — Delete a to-do item.

Sample Create:
POST /api/todos/
{
  "title": "Write docs",
  "description": "Add README for API",
  "is_completed": false,
  "due_date": "2025-12-31",
  "priority": 2
}

Sample Response (201):
{
  "id": 1,
  "title": "Write docs",
  "description": "Add README for API",
  "is_completed": false,
  "due_date": "2025-12-31",
  "priority": 2,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}

Notes:
- Priority must be between 1 and 5 (inclusive).
- No authentication is required.
- Swagger UI available at /docs
- Theme: Ocean Professional (blue #2563EB & amber #F59E0B accents).
