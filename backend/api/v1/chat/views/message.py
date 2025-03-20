from functools import cached_property
from typing import Any

from django.db.models import QuerySet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

from api.common.permissions import HasUserPerms, IsAuthenticatedAndVerified
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseGenericViewSet, ExCreateModelMixin, SerializerViewSetMixin
from api.v1.chat.serializers import MessageRequestModelSerializer, MessageResponseModelSerializer
from apps.chat.models import Chat, Message
from apps.chat.services import MessageCreateService
from apps.chat.services.message import MessageGetService


__all__ = ['MessageViewSet']

from project_selectors.chat.message import get_message_queryset_for_chat


class MessageViewSet(
    SerializerViewSetMixin,
    ExCreateModelMixin,
    BaseGenericViewSet,
    mixins.ListModelMixin,
):
    """ViewSet сообщений."""

    permission_classes = [IsAuthenticatedAndVerified, HasUserPerms]

    serializers = SerializerMapping(
        list=SerializerTypeMapping(
            response=MessageResponseModelSerializer,
            request=MessageResponseModelSerializer,
        ),
        create=SerializerTypeMapping(
            response=MessageResponseModelSerializer,
            request=MessageRequestModelSerializer,
        ),
        actions={
            'new_messages': SerializerTypeMapping(
                response=MessageResponseModelSerializer,
                request=MessageResponseModelSerializer,
            ),
            'previous_messages': SerializerTypeMapping(
                response=MessageResponseModelSerializer,
                request=MessageResponseModelSerializer,
            ),
        },
    )

    @cached_property
    def get_chat_object(self) -> Chat:
        chat_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(Chat, pk=chat_id)
        self.check_object_permissions(self.request, chat)
        return chat

    def get_queryset(self) -> QuerySet:
        return get_message_queryset_for_chat(chat_id=self.get_chat_object.id)

    def perform_create(self, serializer: ModelSerializer) -> Message:
        data = serializer.data
        data['chat'] = self.get_chat_object
        data['sender'] = self.request.user
        return MessageCreateService.from_dict(data).create()

    def list(
        self,
        request: Request,
        *args: Any,
        **kwargs: Any,
    ) -> Response:
        chat = self.get_chat_object
        service = MessageGetService(
            user=request.user,
            chat=chat,
        )
        queryset = service.get_list_by_last_read()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='new-messages/(?P<message_id>[^/.]+)')
    def new_messages(self, request: Request, message_id: int, *args: Any, **kwargs: Any) -> Response:
        """Возвращает новые сообщения, отправленные после указанного сообщения."""
        chat = self.get_chat_object
        message = get_object_or_404(Message, pk=message_id)

        service = MessageGetService(chat=chat, user=request.user)
        new_messages = service.get_new_massages(message=message)
        serializer = self.get_serializer(new_messages, many=True)

        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='previous-messages/(?P<message_id>[^/.]+)')
    def previous_messages(self, request: Request, message_id: int, *args: Any, **kwargs: Any) -> Response:
        """Возвращает предыдущие сообщения, отправленные до указанного сообщения."""
        chat = self.get_chat_object
        message = get_object_or_404(Message, pk=message_id)

        service = MessageGetService(chat=chat, user=request.user)
        previous_messages = service.get_previous_massages(message=message)
        serializer = self.get_serializer(previous_messages, many=True)

        return Response(serializer.data)
