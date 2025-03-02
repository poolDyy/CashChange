from django.db import models

__all__ = ['StatusChoices']


class StatusChoices(models.TextChoices):
    """Статусы записей моделей наследников от BaseModel."""

    PUBLISHED = 'published', 'Опубликовано'
    ARCHIVED = 'archived', 'Архивировано'
