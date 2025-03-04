from api.common.views import BaseGenericViewSet
from api.v1.telegram.permissions import IsTelegramBot
from api.v1.telegram.serializers import (
    TelegramUserModelSerializer,
    TelegramUserVerificationCodeSerializer,
)
from api.v1.telegram.serializers.telegram_user import TelegramUserIsVerifiedSerializer
from apps.telegram.models import TelegramUser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

__all__ = ['TelegramUserViewSet']

from apps.users.models import VerificationCodeTelegram


class TelegramUserViewSet(
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

        verify_code_telegram = VerificationCodeTelegram.objects.filter(
            telegram_username=serializer.data.get('telegram_username'),
        ).first()

        return Response(
            data={'code': verify_code_telegram.code},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=['post'], url_path='is-verified')
    def is_verified(self, request: Request) -> Response:
        serializer = TelegramUserIsVerifiedSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        return Response({'is_verified': serializer.is_valid()}, status=status.HTTP_200_OK)
