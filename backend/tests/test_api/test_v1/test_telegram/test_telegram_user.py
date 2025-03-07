import pytest

from rest_framework import status

from apps.telegram.models import TelegramUser


@pytest.mark.django_db
class TestTelegramUserVerificationCode:
    BASE_URL = '/api/v1/telegram/user/'
    VERIFICATION_CODE_URL = '/api/v1/telegram/user/verification-code/'

    # /api/v1/telegram/user/
    def test_create_telegram_user_success(self, telegram_api_test_client, telegram_user_data):
        """Телеграм-бот должен успешно создавать пользователя (201 Created)."""

        response = telegram_api_test_client.post(
            self.BASE_URL,
            data=telegram_user_data,
        )
        assert TelegramUser.objects.filter(telegram_id=telegram_user_data['telegram_id']).exists()
        assert response['telegram_id'] == telegram_user_data['telegram_id']
        assert response['telegram_username'] == telegram_user_data['telegram_username']

    def test_get_telegram_user_success(self, telegram_api_test_client, telegram_user):
        """Телеграм-бот должен успешно создавать пользователя (201 Created)."""

        telegram_api_test_client.get(
            f'{self.BASE_URL}{telegram_user.telegram_id}/',
        )


    def test_create_telegram_user_missing_telegram_id(self, telegram_api_test_client, telegram_user_data):
        """Запрос без telegram_id должен возвращать 400 Bad Request."""
        telegram_user_data.pop('telegram_id')

        telegram_api_test_client.post(
            self.BASE_URL,
            data=telegram_user_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

    def test_create_telegram_user_duplicate_id(self, telegram_api_test_client, telegram_user, telegram_user_data):
        """Попытка создания пользователя с уже существующим telegram_id должна вернуть 400 Bad Request."""
        telegram_user_data['telegram_id'] = telegram_user.telegram_id

        telegram_api_test_client.post(
            self.BASE_URL,
            data=telegram_user_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

    def test_create_telegram_user_invalid_username(self, telegram_api_test_client, telegram_user_data):
        """Запрос с некорректным username должен возвращать 400 Bad Request."""
        telegram_user_data['telegram_username'] = '@invalid username'

        telegram_api_test_client.post(
            self.BASE_URL,
            data=telegram_user_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

    # /api/v1/telegram/user/verification-code/
    def test_get_verification_code_success(self, telegram_api_test_client, telegram_user, verification_code):
        """Телеграм-бот должен получать код верификации (200 OK)."""
        data = {'telegram_username': telegram_user.telegram_username}

        response = telegram_api_test_client.post(
            self.VERIFICATION_CODE_URL,
            data=data,
            expected_status=status.HTTP_200_OK,
        )
        assert response['code'] == verification_code.code

    def test_get_verification_code_invalid_username(self, telegram_api_test_client):
        """Запрос с несуществующим telegram_username должен возвращать 400 Bad Request."""
        data = {'telegram_username': '@nonexistent_user'}

        telegram_api_test_client.post(
            self.VERIFICATION_CODE_URL,
            data=data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

    def test_get_verification_code_missing_username(self, telegram_api_test_client):
        """Запрос без telegram_username должен возвращать 400 Bad Request."""
        telegram_api_test_client.post(
            self.VERIFICATION_CODE_URL,
            data={},
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

    def test_get_verification_code_unauthorized(self, api_test_client):
        """Запрос без Telegram Bot Token должен возвращать 401 Unauthorized."""
        data = {'telegram_username': 'testuser'}

        api_test_client.post(
            self.VERIFICATION_CODE_URL,
            data=data,
            expected_status=status.HTTP_401_UNAUTHORIZED,
        )
