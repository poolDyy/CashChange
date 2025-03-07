from rest_framework import serializers

from api.common.validatiors import validate_telegram_username, validate_telegram_username_is_not_verified
from apps.telegram.models import TelegramUser


__all__ = [
    'TelegramUserModelSerializer',
    'TelegramUserVerificationCodeSerializer',
]

from apps.users.models import User


class TelegramUserModelSerializer(serializers.ModelSerializer):
    """Сериализатор для модели TelegramUser."""

    is_verified = serializers.SerializerMethodField()

    class Meta:
        model = TelegramUser
        fields = (
            'id',
            'telegram_id',
            'telegram_username',
            'is_verified',
        )
        extra_kwargs = {'telegram_username': {'validators': [validate_telegram_username]}}

    def get_is_verified(self, obj: TelegramUser) -> bool:
        return User.objects.filter(telegram_user=obj, is_verified=True).exists()


class TelegramUserVerificationCodeSerializer(
    serializers.Serializer,
):
    """Сериализатор для получения кода верификации."""

    telegram_username = serializers.CharField(
        required=True,
        max_length=255,
        validators=[validate_telegram_username, validate_telegram_username_is_not_verified],
    )
