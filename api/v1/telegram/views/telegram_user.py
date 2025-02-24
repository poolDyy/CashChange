from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response

from api.common.views import BaseGenericViewSet
from api.v1.telegram.serializers import (
    TelegramUserModelSerializer,
    TelegramUserVerifyCodeRequestSerializer,
    TelegramUserVerifyCodeResponseSerializer,
)
from apps.telegram.models import TelegramUser
from repository import RepoMixin


class TelegramUserViewSet(
    RepoMixin,
    CreateModelMixin,
    BaseGenericViewSet,
):
    """ViewSet для работы с пользователями telegram."""

    serializer_class = TelegramUserModelSerializer
    queryset = TelegramUser.objects.all()

    @action(detail=False, methods=['get'])
    def verify_code(self, request: Request) -> Response:
        """Получение кода верификации."""
        serializer = TelegramUserVerifyCodeRequestSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        serializer.is_valid(raise_exception=True)

        verify_code_telegram = self.repo.users.verification_code_telegram.get_first_by_telegram_username(
            telegram_username=serializer.data.get('telegram_username'),
        )

        response_serializer = TelegramUserVerifyCodeResponseSerializer(
            data={'code': getattr(verify_code_telegram, 'code')},
            context=self.get_serializer_context(),
        )
        response_serializer.is_valid(raise_exception=True)

        return Response(
            data=response_serializer.data,
            status=status.HTTP_200_OK,
        )
