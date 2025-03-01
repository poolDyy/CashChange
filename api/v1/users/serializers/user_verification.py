from rest_framework import serializers

from api.common.validatiors import validate_telegram_username
from apps.users.models import VerificationCodeTelegram

__all__ = [
    'VerificationCodeTelegramCreateModelSerializer',
    'VerificationCodeTelegramCheckRequestSerializer',
    'VerificationCodeTelegramCheckResponseSerializer',
]

from apps.users.services.user_verification import VerificationService


class VerificationCodeTelegramCreateModelSerializer(serializers.ModelSerializer):
    """Сериализатор создания кода верификации."""

    class Meta:
        model = VerificationCodeTelegram
        fields = ('telegram_username',)
        extra_kwargs = {'telegram_username': {'validators': [validate_telegram_username]}}


class VerificationCodeTelegramCheckRequestSerializer(serializers.Serializer):
    """Сериализатор для проверки кода верификации."""

    telegram_username = serializers.CharField(
        max_length=255,
        validators=[validate_telegram_username],
    )
    code = serializers.CharField(
        max_length=6,
        min_length=6,
    )

    def validate(self, attrs: dict) -> dict:
        code = attrs.get('code')
        telegram_username = attrs.get('telegram_username')
        service = VerificationService()

        if service.verify_telegram_code(code=code, telegram_username=telegram_username):
            return attrs

        raise serializers.ValidationError(',\n'.join(service.messages))


class VerificationCodeTelegramCheckResponseSerializer(serializers.Serializer):
    """Сериализатор для проверки кода верификации."""

    is_success = serializers.BooleanField()
    message = serializers.CharField(max_length=255)
