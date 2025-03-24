from datetime import timedelta

import jwt

from django.conf import settings
from django.utils import timezone


__all__ = ['CentrifugoTokenService']


class CentrifugoTokenService:
    """Класс для работы с токенами центрифуги."""

    CENTIFUGO_SECRET = settings.CENTIFUGO_SECRET

    @classmethod
    def generate_token(
        cls,
        user_id: int,
        minutes: int,
        data: dict = None,
    ) -> str:
        if data is None:
            data = {}
        expiration_time = timezone.now() + timedelta(minutes=minutes)

        payload = {
            'sub': str(user_id),
            'exp': int(expiration_time.timestamp()),
            **data,
        }

        return jwt.encode(payload, cls.CENTIFUGO_SECRET, algorithm='HS256')
