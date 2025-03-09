from django.db import models

from apps.common.models import BaseModel


__all__ = ['Currency']


class Currency(BaseModel):
    """Валюта."""

    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Валюта',
    )

    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Код',
    )

    class Meta:
        ordering = ('code',)
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
