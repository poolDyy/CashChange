from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

from apps.common.models import BaseModel


__all__ = ['Attachment']


class Attachment(BaseModel):
    """Модель для хранения вложений."""

    content_type_choices = Q(
        app_label='chat',
        model__in=['message'],
    ) | Q(
        app_label='offers',
        model__in=['offer'],
    )

    message = models.ForeignKey(
        to='chat.Message',
        related_name='attachments',
        on_delete=models.CASCADE,
        verbose_name='Сообщение',
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=content_type_choices,
        verbose_name='Тип вложения',
    )

    object_id = models.PositiveIntegerField(
        verbose_name='ID объекта',
    )

    content_object = GenericForeignKey(
        'content_type',
        'object_id',
    )

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
        ordering = ['-created_at', 'id']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['message']),
        ]

    def __str__(self) -> str:
        return f'Вложение {self.id} ({self.content_type})'
