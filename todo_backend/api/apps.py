from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    App configuration for API layer of the To-Do backend.
    Ocean Professional theme: clean and minimal, blue & amber accents.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
