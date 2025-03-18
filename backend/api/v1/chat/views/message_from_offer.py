from functools import cached_property

from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer

from api.common.permissions import IsAuthenticatedAndVerified
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseGenericViewSet, ExCreateModelMixin, SerializerViewSetMixin
from api.v1.chat.serializers.message import (
    MessageFromOfferRequestModelSerializer,
    MessageFromOfferResponseModelSerializer,
)
from apps.chat.models import Message


__all__ = ['MessageFromOfferModelViewSet']

from apps.chat.services.message import MessageCreateFromOfferService
from apps.offers.models import Offer


class MessageFromOfferModelViewSet(
    SerializerViewSetMixin,
    ExCreateModelMixin,
    BaseGenericViewSet,
):
    """Создание сообщения через предложение."""

    permission_classes = [IsAuthenticatedAndVerified]

    serializers = SerializerMapping(
        create=SerializerTypeMapping(
            response=MessageFromOfferResponseModelSerializer,
            request=MessageFromOfferRequestModelSerializer,
        ),
    )

    @cached_property
    def get_offer_object(self) -> Offer:
        chat_id = self.kwargs.get('offer_id')
        return get_object_or_404(Offer, pk=chat_id)

    def perform_create(self, serializer: ModelSerializer) -> Message:
        data = serializer.data
        data['sender'] = self.request.user
        data['offer'] = self.get_offer_object
        return MessageCreateFromOfferService.from_dict(data).create()
