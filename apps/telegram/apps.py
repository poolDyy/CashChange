from django.apps import AppConfig


class TelegramConfig(AppConfig):
    """Конфигурация приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.telegram'
    label = 'telegram'
