from typing import Any

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.centrifugo.services.token import CentrifugoTokenService


__all__ = ['CentrifugoTokenView']


class CentrifugoTokenView(APIView):
    """Токен для Центрифуги."""

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = request.user

        token = CentrifugoTokenService.generate_token(
            user_id=user.id,
            minutes=60,
        )

        return Response({'token': token}, status=status.HTTP_200_OK)
