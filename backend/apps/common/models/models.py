from django.conf import settings
from django.db import models

from apps.common.models.choices import StatusChoices
from apps.common.models.managers import ArchivedManager, PublishedManager


__all__ = [
    'TimeStampedModel',
    'BaseModel',
]


class TimeStampedModel(models.Model):
    """Абстрактный класс. Содержит `статус` и `время создания / модификации` объекта."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        abstract = True
        ordering = ['-created']


class BaseModel(TimeStampedModel):
    """Абстрактный базовый класс моделей."""

    StatusChoices = StatusChoices

    status = models.CharField(
        verbose_name='Статус',
        max_length=20,
        choices=StatusChoices,
        default=StatusChoices.PUBLISHED,
    )

    updated_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name='Пользователь внесший изменения',
        null=True,
    )

    objects = models.Manager()
    published = PublishedManager()
    archived = ArchivedManager()

    class Meta:
        abstract = True
        ordering = ['-created']

    def user_obj_permission(self, user_id: int) -> bool:
        raise NotImplementedError('Необходимо переопределить user_obj_permission')
