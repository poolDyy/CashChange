from django.db import models

from apps.common.models import BaseModel


__all__ = ['Chat']


class Chat(BaseModel):
    """Чат."""

    title = models.CharField(
        max_length=255,
        verbose_name='Название',
    )

    members = models.ManyToManyField(
        to='users.User',
        through='chat.ChatMember',
        through_fields=('chat', 'user'),
        related_name='chats',
        verbose_name='Участники',
    )

    last_message_date = models.DateTimeField(
        verbose_name='Дата последнего сообщения.',
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-last_message_date']

    def __str__(self) -> str:
        return f'{self.pk}: {self.title}'

    def user_obj_permission(self, user_id: int) -> bool:
        return user_id in self.members.values_list('id', flat=True)
