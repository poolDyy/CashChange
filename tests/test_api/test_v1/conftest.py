import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user(mixer):
    """Создает пользователя."""
    return mixer.blend(User)


@pytest.fixture(scope='module')
def user_data():
    """Тестовые данные для пользователя."""
    return {
        'username': 'testuser',
        'name': 'Test User',
        'password': 'TestPassword123!',
        'repeat_password': 'TestPassword123!',
    }
