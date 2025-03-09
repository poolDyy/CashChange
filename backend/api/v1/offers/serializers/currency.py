from rest_framework import serializers

from apps.offers.models import Currency


__all__ = [
    'CurrencyListRetrieveSerializer',
]


class CurrencyListRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор валюты."""

    class Meta:
        model = Currency
        fields = (
            'id',
            'title',
            'code',
        )
