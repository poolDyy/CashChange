from django.db import models

from apps.common.models import TimeStampedModel

__all__ = ['TelegramUser']


class TelegramUser(TimeStampedModel):
    """Информация о Telegram пользователе."""

    telegram_id = models.CharField(
        verbose_name='ID Telegram',
        max_length=100,
        unique=True,
    )

    telegram_username = models.CharField(
        verbose_name='Никнейм в Telegram',
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = 'Пользователь Telegram'
        verbose_name_plural = 'Пользователи Telegram'
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=models.Q(telegram_username__startswith='@'),
                name='tu_telegram_username_contains_at',
            ),
        ]

    def __str__(self) -> str:
        return self.telegram_username
