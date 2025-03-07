from django.apps import AppConfig


class OffersConfig(AppConfig):
    """Приложение предложений."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.offers'
    label = 'offers'
