from django.db import models

from apps.common.models import TimeStampedModel

__all__ = ['VerificationCodeTelegram']


class VerificationCodeTelegram(TimeStampedModel):
    """Код верификации пользователя."""

    code = models.CharField(
        verbose_name='Код верификации',
        max_length=6,
        editable=False,
    )

    telegram_username = models.CharField(
        verbose_name='Никнейм в Telegram',
        max_length=255,
        editable=False,
    )

    class Meta:
        verbose_name = 'Код верификации пользователя.'
        verbose_name_plural = 'Коды верификации пользователя.'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['code', 'telegram_username'],
                name='unique_code_per_telegram_username',
            )
        ]
