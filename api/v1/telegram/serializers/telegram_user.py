from rest_framework import serializers

from apps.telegram.models import TelegramUser

__all__ = [
    'TelegramUserModelSerializer',
    'TelegramUserVerifyCodeRequestSerializer',
    'TelegramUserVerifyCodeResponseSerializer',
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


class TelegramUserVerifyCodeRequestSerializer(serializers.Serializer):
    """Сериализатор для получения кода верификации."""

    telegram_username = serializers.CharField(
        required=True,
        max_length=255,
    )


class TelegramUserVerifyCodeResponseSerializer(serializers.Serializer):
    """Сериализатор для получения кода верификации."""

    code = serializers.CharField(
        required=True,
        max_length=6,
        min_length=6,
    )
