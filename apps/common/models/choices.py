from django.db import models

__all__ = ['StatusChoices']


class StatusChoices(models.TextChoices):
    PUBLISHED = 'published', 'Опубликовано'
    ARCHIVED = 'archived', 'Архивировано'
