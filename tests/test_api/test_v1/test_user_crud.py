import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

BASE_URL = '/api/v1/users/'


@pytest.mark.django_db
def test_get_user_list(api_client, user):
    """Тест получения списка пользователей."""
    response = api_client.get(BASE_URL)
    assert isinstance(response, list)
    assert any(u['id'] == user.id for u in response)


@pytest.mark.django_db
def test_get_user_detail(api_client, user):
    """Тест получения одного пользователя."""
    response = api_client.get(f'{BASE_URL}{user.id}/')
    assert response['id'] == user.id
    assert response['username'] == user.username


@pytest.mark.django_db
def test_create_user(api_client, user_data):
    """Тест создания пользователя."""
    response = api_client.post(BASE_URL, data=user_data)

    created_user = User.objects.get(id=response['id'])
    assert created_user.username == user_data['username']
    assert created_user.name == user_data['name']


@pytest.mark.django_db
def test_create_user_password_mismatch(api_client, user_data):
    """Тест ошибки при несовпадении паролей."""
    user_data['repeat_password'] = 'WrongPassword'
    api_client.post(BASE_URL, data=user_data, expected_status=status.HTTP_400_BAD_REQUEST)


@pytest.mark.django_db
def test_update_user(auth_api_client, user):
    """Тест обновления пользователя."""
    new_name = 'Updated Name'
    response = auth_api_client.put(f'{BASE_URL}{user.id}/', data={'name': new_name})

    user.refresh_from_db()
    assert user.name == new_name
    assert response['name'] == new_name


@pytest.mark.django_db
def test_partial_update_user(auth_api_client, user):
    """Тест частичного обновления пользователя."""
    new_name = 'Partially Updated'
    response = auth_api_client.patch(f'{BASE_URL}{user.id}/', data={'name': new_name})

    user.refresh_from_db()
    assert user.name == new_name
    assert response['name'] == new_name


@pytest.mark.django_db
def test_delete_user(auth_api_client, user):
    """Тест удаления пользователя."""
    auth_api_client.delete(f'{BASE_URL}{user.id}/')
    assert not User.objects.filter(id=user.id).exists()
