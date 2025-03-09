from django.db import models

from apps.common.models import BaseModel


__all__ = ['Feedback']


class Feedback(BaseModel):
    """Обратная связь."""

    email = models.EmailField(
        max_length=255,
        verbose_name='Почта',
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок',
    )

    description = models.TextField(
        verbose_name='Описание',
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-created_at']
