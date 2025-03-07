import pytest

from mixer.backend.django import mixer as _mixer

from apps.telegram.models import TelegramUser
from apps.users.models import User

from .common import ApiTestClient, ApiTestClientAuth, ApiTestClientTelegram


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def api_test_client():
    return ApiTestClient()


def create_user(mixer, **kwargs):
    password = kwargs.pop('password', 'testpassword123!')
    user = mixer.blend(User, **kwargs)
    user.set_password(password)
    user.save()
    return user


@pytest.fixture
def auth_user(mixer):
    """Фикстура для создания тестового пользователя."""
    return create_user(mixer, username='testuser', telegram_user=None)


@pytest.fixture
def telegram_user(mixer):
    return mixer.blend(TelegramUser, telegram_username='testuser', telegram_id='1111')


@pytest.fixture
def unverified_user(mixer):
    """Создает пользователя, который НЕ прошел верификацию."""
    return create_user(mixer, username='testuser', is_verified=False, telegram_user=None)


@pytest.fixture
def verified_user(mixer, telegram_user):
    """Создает пользователя, который уже верифицирован."""
    return create_user(mixer, username='testuser', is_verified=True, telegram_user=telegram_user)


@pytest.fixture
def auth_api_test_client(auth_user):
    """Фикстура для создания авторизованного клиента."""
    return ApiTestClientAuth(
        user=auth_user,
    )


@pytest.fixture
def auth_api_client_unverified(unverified_user):
    """Фикстура для авторизованного клиента с НЕверифицированным пользователем."""
    return ApiTestClientAuth(user=unverified_user)


@pytest.fixture
def auth_api_client_verified(verified_user):
    """Фикстура для авторизованного клиента с верифицированным пользователем."""
    return ApiTestClientAuth(user=verified_user)


@pytest.fixture
def telegram_api_test_client():
    """Фикстура для создания клиента телеграм бота."""
    return ApiTestClientTelegram()
