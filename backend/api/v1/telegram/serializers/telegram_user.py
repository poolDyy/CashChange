from api.common.validatiors import validate_telegram_username, validate_telegram_username_is_not_verified
from apps.telegram.models import TelegramUser
from rest_framework import serializers

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


class TelegramUserVerificationCodeSerializer(
    serializers.Serializer,
):
    """Сериализатор для получения кода верификации."""

    telegram_username = serializers.CharField(
        required=True,
        max_length=255,
        validators=[validate_telegram_username, validate_telegram_username_is_not_verified],
    )


class TelegramUserIsVerifiedSerializer(
    serializers.Serializer,
):
    """Сериализатор для проверки верификации пользователя."""

    telegram_username = serializers.CharField(
        required=True,
        max_length=255,
        validators=[validate_telegram_username, validate_telegram_username_is_not_verified],
    )
