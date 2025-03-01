import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserCRUD:
    BASE_URL = '/api/v1/users/user/'

    def test_get_user_list(self, api_test_client, user):
        """Тест получения списка пользователей."""
        response = api_test_client.get(self.BASE_URL)
        assert isinstance(response, list)
        assert any(u['id'] == user.id for u in response)

    def test_get_user_detail(self, api_test_client, user):
        """Тест получения одного пользователя."""
        response = api_test_client.get(f'{self.BASE_URL}{user.id}/')
        assert response['id'] == user.id
        assert response['username'] == user.username

    def test_create_user(self, api_test_client, user_data):
        """Тест создания пользователя."""
        response = api_test_client.post(self.BASE_URL, data=user_data)

        created_user = User.objects.get(id=response['id'])
        assert created_user.username == user_data['username']
        assert created_user.name == user_data['name']

    def test_create_user_password_mismatch(self, api_test_client, user_data):
        """Тест ошибки при несовпадении паролей."""
        user_data['repeat_password'] = 'WrongPassword'
        api_test_client.post(self.BASE_URL, data=user_data, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_update_user(self, auth_api_test_client, user):
        """Тест обновления пользователя."""
        new_name = 'Updated Name'
        response = auth_api_test_client.put(f'{self.BASE_URL}{user.id}/', data={'name': new_name})

        user.refresh_from_db()
        assert user.name == new_name
        assert response['name'] == new_name

    def test_partial_update_user(self, auth_api_test_client, user):
        """Тест частичного обновления пользователя."""
        new_name = 'Partially Updated'
        response = auth_api_test_client.patch(f'{self.BASE_URL}{user.id}/', data={'name': new_name})

        user.refresh_from_db()
        assert user.name == new_name
        assert response['name'] == new_name

    def test_delete_user(self, auth_api_test_client, user):
        """Тест удаления пользователя."""
        auth_api_test_client.delete(f'{self.BASE_URL}{user.id}/')
        assert not User.objects.filter(id=user.id).exists()
