from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.common.enums import SerializerType
from api.common.permissions import IsAuthenticatedAndNotVerified
from api.common.types import SerializerMapping, SerializerTypeMapping
from api.common.views import BaseGenericViewSet, ExCreateModelMixin, SerializerViewSetMixin
from api.v1.users.serializers import (
    VerificationCodeTelegramCheckRequestSerializer,
    VerificationCodeTelegramCheckResponseSerializer,
    VerificationCodeTelegramCreateModelSerializer,
)
from apps.users.models import VerificationCodeTelegram
from repository import RepoMixin

__all__ = ['VerificationCodeTelegramCreateViewSet']


class VerificationCodeTelegramCreateViewSet(
    RepoMixin,
    SerializerViewSetMixin,
    ExCreateModelMixin,
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
                request=VerificationCodeTelegramCheckRequestSerializer,
                response=VerificationCodeTelegramCheckResponseSerializer,
            )
        },
    )

    queryset = VerificationCodeTelegram.objects.all()

    def perform_create(
        self,
        serializer: VerificationCodeTelegramCreateModelSerializer,
    ) -> VerificationCodeTelegram:
        return self.repo.users.verification_code_telegram.create(
            telegram_username=serializer.data.get('telegram_username')
        )

    @action(detail=False, methods=['post'])
    def verify(self, request: Request) -> Response:
        """Верификация пользователя."""
        serializer = self.get_serializer(data=request.data, type_=SerializerType.REQUEST)
        serializer.is_valid(raise_exception=True)

        telegram_username = serializer.data.get('telegram_username')

        self.repo.users.user.add_telegram_user_to_user(
            telegram_username=telegram_username,
            user=request.user,
        )
        return Response(
            data={
                'is_success': True,
                'message': 'Верификация пройдена успешно',
            },
            status=status.HTTP_200_OK,
        )
