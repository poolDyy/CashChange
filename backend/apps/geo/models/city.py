from django.db import models


class City(models.Model):
    """Город."""

    title = models.CharField(
        max_length=255,
        verbose_name='Город',
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
