from functools import cached_property
from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common.permissions import HasUserPerms
from apps.centrifugo.services.broadcasts import ChatBroadcastService
from apps.centrifugo.services.token import CentrifugoTokenService
from apps.chat.models import Chat


class ChatWSConnectionView(APIView):
    """Ручка подключения к каналу счетчика сообщений."""

    permission_classes = [IsAuthenticated, HasUserPerms]

    @cached_property
    def get_chat_object(self) -> Chat:
        chat_id = self.kwargs.get('id')
        chat = get_object_or_404(Chat, pk=chat_id)
        self.check_object_permissions(self.request, chat)
        return chat

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        chat = self.get_chat_object
        channel = ChatBroadcastService.get_channel(chat.id)
        token = CentrifugoTokenService.generate_token(
            user_id=request.user.id,
            minutes=5,
            data={
                'channel': channel,
            },
        )
        return Response({'token': token}, status=status.HTTP_200_OK)
