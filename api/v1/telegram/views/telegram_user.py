from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from api.common.views import BaseGenericViewSet
from api.v1.telegram.permissions import IsTelegramBot
from api.v1.telegram.serializers import (
    TelegramUserModelSerializer,
    TelegramUserVerificationCodeSerializer,
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

    @action(detail=False, methods=['post'], url_path='verification-code')
    def verification_code(self, request: Request) -> Response:
        """Получение кода верификации."""
        serializer = TelegramUserVerificationCodeSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        verify_code_telegram = self.repo.users.verification_code_telegram.get_first_by_telegram_username(
            telegram_username=serializer.data.get('telegram_username'),
        )

        if verify_code_telegram is None:
            return Response(
                {'code': 'По Вашему username не найден код верификации'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data={'code': verify_code_telegram.code},
            status=status.HTTP_200_OK,
        )
