from rest_framework import serializers

from api.common.serializers import BaseSerializer
from apps.geo.models import City
from apps.offers.models import Currency, Offer
from apps.users.models import User


__all__ = [
    'OfferListRetrieveResponseModelSerializer',
    'OfferCreateUpdateRequestSerializer',
]


class CurrencyOfferSerializer(serializers.ModelSerializer):
    """Сериализатор валюты для предложения."""

    class Meta:
        model = Currency
        fields = (
            'id',
            'code',
        )


class CityOfferSerializer(serializers.ModelSerializer):
    """Сериализатор города для предложения."""

    class Meta:
        model = City
        fields = (
            'id',
            'name',
        )


class UserOfferModelSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя для предложения."""

    class Meta:
        model = User
        fields = (
            'id',
            'name',
        )


class OfferListRetrieveResponseModelSerializer(BaseSerializer):
    """Сериализатор предложения для одного и нескольких объектов."""

    user = UserOfferModelSerializer
    city = CityOfferSerializer
    currency = CurrencyOfferSerializer

    offer_type = serializers.CharField(source='get_offer_type_display')

    class Meta:
        model = Offer
        fields = (
            'id',
            'title',
            'description',
            'user',
            'city',
            'currency',
            'cost',
            'min_value',
            'max_value',
            'offer_type',
        )


class OfferCreateUpdateRequestSerializer(BaseSerializer):
    """Сериализатор для создания, редактирования предложения."""

    class Meta:
        model = Offer
        fields = (
            'id',
            'title',
            'description',
            'user',
            'city',
            'currency',
            'cost',
            'min_value',
            'max_value',
            'offer_type',
        )
