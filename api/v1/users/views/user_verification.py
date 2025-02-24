from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.common.enums import SerializerType
from api.common.permissions import IsAuthenticatedAndNotVerified
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseGenericViewSet, ExCreateModelMixin, SerializerViewSetMixin
from api.v1.users.serializers import (
    VerificationCodeTelegramCheckRequestModelSerializer,
    VerificationCodeTelegramCheckResponseSerializer,
    VerificationCodeTelegramCreateModelSerializer,
)
from apps.users.models import VerificationCodeTelegram
from apps.users.services.user_verification import VerificationCodeCreateService
from repository import RepoMixin


class VerificationCodeTelegramCreateViewSet(
    RepoMixin,
    ExCreateModelMixin,
    SerializerViewSetMixin,
    BaseGenericViewSet,
):
    """Создание кода верификации."""

    permission_classes = [IsAuthenticatedAndNotVerified]

    serializers = SerializerMapping(
        create=SerializerTypeMapping(
            request=VerificationCodeTelegramCreateModelSerializer,
            response=VerificationCodeTelegramCreateModelSerializer,
        ),
        actions={
            'verify': SerializerTypeMapping(
                request=VerificationCodeTelegramCheckRequestModelSerializer,
                response=VerificationCodeTelegramCheckResponseSerializer,
            )
        },
    )

    queryset = VerificationCodeTelegram.objects.all()

    def perform_create(
        self,
        serializer: VerificationCodeTelegramCreateModelSerializer,
    ) -> VerificationCodeTelegram:
        return VerificationCodeCreateService.create_verification_code(
            telegram_username=serializer.data.get('telegram_username')
        )

    @action(detail=False, methods=['post'])
    def verify(self, request: Request) -> Response:
        """Верификация пользователя."""
        serializer = self.get_serializer(data=request.data, type_=SerializerType.REQUEST)
        serializer.is_valid(raise_exception=True)

        telegram_username = serializer.data.get('telegram_username')
        try:
            self.repo.users.user.add_telegram_user_to_user(
                telegram_username=telegram_username,
                user=request.user,
            )
        except ValueError:
            raise serializers.ValidationError(f'Не найден пользователь telegram с именем: {telegram_username}')
        response_serializer = self.get_serializer(
            data={
                'is_success': True,
                'message': 'Верификация пройдена успешно',
            },
            type_=SerializerType.RESPONSE,
        )
        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK,
        )
