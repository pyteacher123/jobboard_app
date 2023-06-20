"""
Core django app configuration module.
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Config class"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
