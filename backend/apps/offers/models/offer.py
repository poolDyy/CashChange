from django.db import models
from django.db.models import Q

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
        max_digits=10,
        decimal_places=2,
        null=True,
    )

    min_value = models.DecimalField(
        verbose_name='Минимальный объем',
        max_digits=12,
        decimal_places=2,
        null=True,
    )

    max_value = models.DecimalField(
        verbose_name='Максимальный объем',
        max_digits=12,
        decimal_places=2,
        null=True,
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
        constraints = [
            models.CheckConstraint(
                check=Q(max_value__gte=models.F('min_value')) | Q(min_value__isnull=True) | Q(max_value__isnull=True),
                name='ofr_check_max_value_gte_min_value',
            ),
        ]
