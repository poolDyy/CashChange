from apps.users.models import User, VerificationCodeTelegram
from rest_framework import serializers


def validate_telegram_username(value: str) -> str:
    """Валидатор для проверки наличия символа @ в telegram_username."""
    if '@' in value:
        raise serializers.ValidationError('Никнейм в Telegram не должен содержать символ @.')
    return value


def validate_telegram_username_is_not_verified(value: str) -> str:
    """Валидатор для проверки верификации пользователя."""
    user = User.objects.filter(telegram_user__telegram_username=value).first()
    if getattr(user, 'is_verified', False):
        raise serializers.ValidationError('Пользователь уже верифицирован.')
    return value


def telegram_username_has_code(value: str) -> str:
    """Валидатор проверяет, что существует код на этот юзернейм."""
    is_exists = VerificationCodeTelegram.objects.filter(
        telegram_username=value,
    ).exists()
    if not is_exists:
        raise serializers.ValidationError('По Вашему username не найден код верификации')
    return value
