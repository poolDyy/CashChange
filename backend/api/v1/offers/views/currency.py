from rest_framework import mixins

from api.common.permissions import ReadOnly
from api.common.views import BaseGenericViewSet
from api.v1.offers.serializers import CurrencyListRetrieveSerializer
from apps.offers.models import Currency


__all__ = [
    'CurrencyViewSet',
]


class CurrencyViewSet(
    BaseGenericViewSet,
    mixins.ListModelMixin,
):
    """ViewSet Валюты."""

    serializer_class = CurrencyListRetrieveSerializer
    queryset = Currency.objects.all()

    permission_classes = [ReadOnly]
