from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
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
from apps.users.services.user_verification import VerificationCodeCreateService, VerificationService


class VerificationCodeTelegramCreateViewSet(
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
        return VerificationCodeCreateService.create_verification_code(
            telegram_username=serializer.data.get('telegram_username')
        )

    @action(detail=False, methods=['post'])
    def verify(self, request: Request) -> Response:
        """Верификация пользователя."""
        serializer = self.get_serializer(data=request.data, type_=SerializerType.REQUEST)
        serializer.is_valid(raise_exception=True)

        telegram_username = serializer.data.get('telegram_username')
        code = serializer.data.get('code')

        service = VerificationService()
        service.verify(telegram_username=telegram_username, code=code, user=request.user)

        if service.is_valid:
            return Response(
                data={
                    'is_success': True,
                    'message': 'Верификация пройдена успешно',
                },
                status=status.HTTP_200_OK,
            )

        raise ValidationError({'non_field_errors': service.errors})
