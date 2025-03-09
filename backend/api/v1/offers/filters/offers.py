import django_filters

from apps.offers.models import Offer


__all__ = ['OfferFilter']


class OfferFilter(django_filters.FilterSet):
    """Фильтр для OfferViewSet."""

    min_value_gte = django_filters.NumberFilter(field_name='min_value', lookup_expr='gte')

    max_value_lte = django_filters.NumberFilter(field_name='max_value', lookup_expr='lte')

    cost_gte = django_filters.NumberFilter(field_name='cost', lookup_expr='gte')
    cost_lte = django_filters.NumberFilter(field_name='cost', lookup_expr='lte')

    offer_type = django_filters.CharFilter(field_name='offer_type')
    currency = django_filters.CharFilter(field_name='currency_id')
    city = django_filters.CharFilter(field_name='city_id')

    class Meta:
        model = Offer
        fields = [
            'min_value_gte',
            'max_value_lte',
            'cost_gte',
            'cost_lte',
            'offer_type',
            'currency',
            'city',
        ]
