from django.db import models

from apps.common.models import BaseModel


__all__ = ['Message']


class Message(BaseModel):
    """Сообщение."""

    sender = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Отправитель',
    )

    chat = models.ForeignKey(
        to='chat.Chat',
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Чат',
    )

    message = models.TextField(
        verbose_name='Текст',
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['chat']),
        ]

    def __str__(self) -> str:
        return f'ID: {self.id}, Чат: {self.chat}, Отправитель: {self.sender} '
