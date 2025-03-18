from django.db import models

from apps.common.models import BaseModel


__all__ = ['ChatMember']


class ChatMember(BaseModel):
    """Участник Чата."""

    chat = models.ForeignKey(
        to='chat.Chat',
        on_delete=models.CASCADE,
        verbose_name='Чат',
    )

    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name='Пользователь',
    )

    last_read_message = models.ForeignKey(
        to='chat.Message',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Последнее прочитанное сообщение',
    )

    class Meta:
        verbose_name = 'Участник чата'
        verbose_name_plural = 'Участники чата'
        ordering = ['-created_at']
        unique_together = ('chat', 'user')
        indexes = [
            models.Index(fields=['chat', 'user']),
        ]

    def __str__(self) -> str:
        return f'{self.chat}: {self.user}'
