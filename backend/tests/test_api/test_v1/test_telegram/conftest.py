import pytest

from apps.users.services.user_verification import VerificationCodeCreateService


@pytest.fixture
def verification_code(telegram_user):
    """Код верификации."""
    return VerificationCodeCreateService.create_verification_code(
        telegram_username=telegram_user.telegram_username,
    )


@pytest.fixture
def telegram_user_data():
    """Тестовые данные для Telegram пользователя."""
    return {
        'telegram_id': '123456789',
        'telegram_username': '@testuser',
    }
