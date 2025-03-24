from typing import Any

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common.permissions import HasUserPerms
from apps.centrifugo.services.broadcasts import MessageCounterBroadcastService
from apps.centrifugo.services.token import CentrifugoTokenService
from apps.chat.services.message import MessageCounterService


class MessageCounterWSConnectionView(APIView):
    """Ручка подключения к каналу счетчика сообщений."""

    permission_classes = [IsAuthenticated, HasUserPerms]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        channel = MessageCounterBroadcastService.get_channel(request.user.id)
        token = CentrifugoTokenService.generate_token(
            user_id=request.user.id,
            minutes=60,
            data={
                'channel': channel,
            },
        )
        counters = MessageCounterService(user=request.user).get_for_response()
        return Response(
            {'token': token, 'counters': counters},
            status=status.HTTP_200_OK,
        )
