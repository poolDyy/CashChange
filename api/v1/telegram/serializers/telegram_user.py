from rest_framework import serializers

from api.common.validatiors import validate_telegram_username
from apps.telegram.models import TelegramUser

__all__ = [
    'TelegramUserModelSerializer',
    'TelegramUserVerificationCodeSerializer',
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
        extra_kwargs = {'telegram_username': {'validators': [validate_telegram_username]}}


class TelegramUserVerificationCodeSerializer(serializers.Serializer):
    """Сериализатор для получения кода верификации."""

    telegram_username = serializers.CharField(
        required=True,
        max_length=255,
        validators=[validate_telegram_username],
    )
