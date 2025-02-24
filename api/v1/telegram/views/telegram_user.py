from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from api.common.views import BaseGenericViewSet
from api.v1.telegram.permissions import IsTelegramBot
from api.v1.telegram.serializers import (
    TelegramUserModelSerializer,
    TelegramUserVerificationCodeRequestSerializer,
    TelegramUserVerificationCodeResponseSerializer,
)
from apps.telegram.models import TelegramUser
from repository import RepoMixin

__all__ = ['TelegramUserViewSet']


class TelegramUserViewSet(
    RepoMixin,
    CreateModelMixin,
    BaseGenericViewSet,
):
    """ViewSet для работы с пользователями telegram."""

    serializer_class = TelegramUserModelSerializer
    queryset = TelegramUser.objects.all()
    permission_classes = [IsTelegramBot]

    @action(detail=False, methods=['get'], url_path='verification-code')
    def verification_code(self, request: Request) -> Response:
        """Получение кода верификации."""
        serializer = TelegramUserVerificationCodeRequestSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        verify_code_telegram = self.repo.users.verification_code_telegram.get_first_by_telegram_username(
            telegram_username=serializer.data.get('telegram_username'),
        )

        response_serializer = TelegramUserVerificationCodeResponseSerializer(
            data={'code': getattr(verify_code_telegram, 'code')},
            context=self.get_serializer_context(),
        )
        response_serializer.is_valid(raise_exception=True)

        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )
