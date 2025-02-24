from rest_framework import serializers

from apps.telegram.models import TelegramUser

__all__ = [
    'TelegramUserModelSerializer',
    'TelegramUserVerificationCodeRequestSerializer',
    'TelegramUserVerificationCodeResponseSerializer',
]


class TelegramUserModelSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TelegramUser."""

    class Meta:
        model = TelegramUser
        fields = (
            'id',
            'telegram_id',
            'telegram_username',
        )


class TelegramUserVerificationCodeRequestSerializer(serializers.Serializer):
    """Сериализатор для получения кода верификации."""

    telegram_username = serializers.CharField(
        required=True,
        max_length=255,
    )


class TelegramUserVerificationCodeResponseSerializer(serializers.Serializer):
    """Сериализатор для получения кода верификации."""

    code = serializers.CharField(
        required=True,
        max_length=6,
        min_length=6,
    )
