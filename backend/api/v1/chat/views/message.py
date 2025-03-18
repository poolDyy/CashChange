from functools import cached_property

from django.db.models import QuerySet
from project_selectors.chat.message import get_message_queryset_for_chat
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer

from api.common.permissions import IsAuthenticatedAndVerified
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseGenericViewSet, ExCreateModelMixin, SerializerViewSetMixin
from api.v1.chat.serializers import MessageRequestModelSerializer, MessageResponseModelSerializer
from apps.chat.models import Chat, Message
from apps.chat.services import MessageCreateService


__all__ = ['MessageViewSet']


class MessageViewSet(
    SerializerViewSetMixin,
    ExCreateModelMixin,
    BaseGenericViewSet,
):
    """ViewSet сообщений."""

    permission_classes = [IsAuthenticatedAndVerified]

    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=MessageResponseModelSerializer,
            request=MessageResponseModelSerializer,
        ),
        create=SerializerTypeMapping(
            response=MessageResponseModelSerializer,
            request=MessageRequestModelSerializer,
        ),
    )

    @cached_property
    def get_chat_object(self) -> Chat:
        chat_id = self.kwargs.get('chat_id')
        return get_object_or_404(Chat, pk=chat_id)

    def get_queryset(self) -> QuerySet:
        return get_message_queryset_for_chat(chat_id=self.get_chat_object.id)

    def perform_create(self, serializer: ModelSerializer) -> Message:
        data = serializer.data
        data['chat'] = self.get_chat_object
        data['sender'] = self.request.user
        return MessageCreateService.from_dict(data).create()
