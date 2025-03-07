from typing import Type

from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet


__all__ = [
    'IsTelegramBot',
]


class IsTelegramBot(BasePermission):
    """Разрешение для телеграм бота."""

    def has_permission(self, request: Request, view: Type[ViewSet]) -> bool:
        telegram_token = request.headers.get('X-Telegram-Bot-Token')

        return telegram_token == settings.TELEGRAM_BOT_SECRET_API_TOKEN
