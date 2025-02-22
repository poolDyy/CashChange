import pytest
from mixer.backend.django import mixer as _mixer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User

from .common import ApiTestClient


@pytest.fixture(scope='session')
def api_client():
    return ApiTestClient()


@pytest.fixture(scope='session')
def mixer():
    return _mixer


@pytest.fixture
def user(mixer):
    """Фикстура для создания тестового пользователя."""
    return mixer.blend(User, username='testuser', password='testpassword123!')


@pytest.fixture
def auth_api_client(user):
    """Фикстура для создания авторизованного клиента."""
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client = ApiTestClient()
    client.api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client
