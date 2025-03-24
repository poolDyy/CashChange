from django.apps import AppConfig


class ChatConfig(AppConfig):
    """Конфиг приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chat'
    label = 'chat'

    def ready(self) -> None:
        from apps.chat.signals import callbacks  # noqa: F401
