import pytest
from django.contrib.auth import get_user_model

from apps.users.services.user_verification import VerificationCodeCreateService

User = get_user_model()


@pytest.fixture
def user(mixer):
    """Создает пользователя."""
    return mixer.blend(User, telegram_user=None)


@pytest.fixture
def user_data():
    """Тестовые данные для пользователя."""
    return {
        'username': 'testuser',
        'name': 'Test User',
        'password': 'TestPassword123!',
        'repeat_password': 'TestPassword123!',
    }


@pytest.fixture
def verification_code(telegram_user):
    """Код верификации."""
    return VerificationCodeCreateService.create_verification_code(
        telegram_username=telegram_user.telegram_username,
    )
