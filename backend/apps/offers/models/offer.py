from django.db import models

from apps.common.models import BaseModel


__all__ = ['Offer']


class Offer(BaseModel):
    """Предложение."""

    class OfferTypeChoices(models.TextChoices):
        """Типы предложений."""

        BUY = 'buy', 'Куплю'
        SELL = 'sell', 'Продам'

    user = models.ForeignKey(
        to='users.User',
        on_delete=models.CASCADE,
        related_name='offers',
        verbose_name='Пользователь',
    )

    city = models.ForeignKey(
        to='geo.City',
        on_delete=models.RESTRICT,
        related_name='offers',
        verbose_name='Город',
    )

    currency = models.ForeignKey(
        to='offers.Currency',
        on_delete=models.RESTRICT,
        related_name='offers',
        verbose_name='Валюта',
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок',
    )

    offer_type = models.CharField(
        max_length=4,
        choices=OfferTypeChoices,
        verbose_name='Тип предложения',
    )

    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )

    cost = models.DecimalField(
        verbose_name='Цена',
        decimal_places=2,
        blank=True,
    )

    min_value = models.DecimalField(
        verbose_name='Минимальный объем',
        decimal_places=6,
        blank=True,
    )

    max_value = models.DecimalField(
        verbose_name='Максимальный объем',
        decimal_places=6,
        blank=True,
    )

    rate = models.SmallIntegerField(
        default=0,
        verbose_name='Рейтинг',
    )

    class Meta:
        ordering = (
            '-rate',
            '-created_at',
        )
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['city']),
            models.Index(fields=['currency']),
        ]
