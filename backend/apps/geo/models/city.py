from django.db import models


__all__ = ['City']


class City(models.Model):
    """Город."""

    name = models.CharField(
        max_length=255,
        verbose_name='Город',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
