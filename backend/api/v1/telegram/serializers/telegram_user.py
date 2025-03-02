from api.common.validatiors import validate_telegram_username
from apps.telegram.models import TelegramUser
from repository import RepoMixin
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
    RepoMixin,
    serializers.Serializer,
):
    """Сериализатор для получения кода верификации."""

    telegram_username = serializers.CharField(
        required=True,
        max_length=255,
        validators=[validate_telegram_username],
    )

    def validate(self, attrs: dict) -> dict:
        telegram_username = attrs['telegram_username']
        if self.repo.users.user.is_verified_by_telegram_username(telegram_username=telegram_username):
            raise serializers.ValidationError('Пользователь уже верифицирован.')
        return attrs
