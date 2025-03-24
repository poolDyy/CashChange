from django.apps import AppConfig


class CentrifugoConfig(AppConfig):
    """Конфиг придложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.centrifugo'
    label = 'centrifugo'
