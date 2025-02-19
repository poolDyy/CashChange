from django.db import models

from apps.common.models.choices import StatusChoices

__all__ = [
    'PublishedManager',
    'ArchivedManager',
]


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=StatusChoices.PUBLISHED)


class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=StatusChoices.ARCHIVED)
