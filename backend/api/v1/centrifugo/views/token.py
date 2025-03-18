from datetime import timedelta
from typing import Any

import jwt

from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


__all__ = ['CentrifugoTokenView']


class CentrifugoTokenView(APIView):
    """Токен для Центрифуги."""

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user = request.user

        expiration_time = timezone.now() + timedelta(hours=1)

        payload = {
            'sub': str(user.id),
            'exp': int(expiration_time.timestamp()),
        }

        token = jwt.encode(payload, settings.CENTIFUGO_SECRET, algorithm='HS256')

        return Response({'token': token}, status=status.HTTP_200_OK)
