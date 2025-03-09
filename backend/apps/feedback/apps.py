from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """Конфиг приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.feedback'
    label = 'feedback'
