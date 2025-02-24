from rest_framework import serializers

from apps.users.models import VerificationCodeTelegram

__all__ = [
    'VerificationCodeTelegramCreateModelSerializer',
    'VerificationCodeTelegramCheckRequestModelSerializer',
    'VerificationCodeTelegramCheckResponseSerializer',
]

from apps.users.services.user_verification import VerificationService


class VerificationCodeTelegramCreateModelSerializer(serializers.ModelSerializer):
    """Сериализатор создания кода верификации."""

    class Meta:
        model = VerificationCodeTelegram
        fields = ('telegram_username',)


class VerificationCodeTelegramCheckRequestModelSerializer(serializers.ModelSerializer):
    """Сериализатор для проверки кода верификации."""

    class Meta:
        model = VerificationCodeTelegram
        fields = (
            'telegram_username',
            'code',
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
