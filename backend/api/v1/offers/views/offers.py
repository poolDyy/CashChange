from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ModelSerializer

from api.common.permissions import HasUserPermsOrReadOnly, IsVerifiedOrReadOnly
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseModelViewSet
from api.v1.offers.filters import OfferFilter
from api.v1.offers.serializers import OfferCreateUpdateRequestSerializer, OfferListRetrieveResponseModelSerializer
from apps.offers.models import Offer


__all__ = ['OfferViewSet']

from apps.offers.services import OfferCreateService, OfferUpdateService


class OfferViewSet(BaseModelViewSet):
    """ViewSet предложения."""

    permission_classes = [IsVerifiedOrReadOnly, HasUserPermsOrReadOnly]

    queryset = Offer.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter

    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=OfferListRetrieveResponseModelSerializer,
            request=OfferListRetrieveResponseModelSerializer,
        ),
        retrieve=SerializerTypeMapping(
            response=OfferListRetrieveResponseModelSerializer,
            request=OfferListRetrieveResponseModelSerializer,
        ),
        create=SerializerTypeMapping(
            response=OfferListRetrieveResponseModelSerializer,
            request=OfferCreateUpdateRequestSerializer,
        ),
        update=SerializerTypeMapping(
            response=OfferListRetrieveResponseModelSerializer,
            request=OfferCreateUpdateRequestSerializer,
        ),
        partial_update=SerializerTypeMapping(
            response=OfferListRetrieveResponseModelSerializer,
            request=OfferCreateUpdateRequestSerializer,
        ),
    )

    def perform_create(self, serializer: ModelSerializer) -> Offer:
        data = serializer.validated_data
        data['user'] = self.request.user
        service = OfferCreateService.from_dict(data=data)
        offer = service.create()
        return offer

    def perform_update(self, serializer: ModelSerializer) -> Offer:
        data = serializer.validated_data
        data['instance'] = serializer.instance
        service = OfferUpdateService.from_dict(data=data)
        offer = service.update()
        return offer
