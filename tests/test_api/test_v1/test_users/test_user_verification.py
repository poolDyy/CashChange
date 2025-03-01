import pytest
from rest_framework import status

from apps.users.models import VerificationCodeTelegram


@pytest.mark.django_db
class TestUserVerification:
    BASE_URL = '/api/v1/users/verification/'
    VERIFY_URL = f'{BASE_URL}verify/'

    def test_create_verification_code_success(
        self,
        auth_api_client_unverified,
    ):
        """Авторизованный, но НЕверифицированный пользователь должен создать код (201 Created)."""
        data = {'telegram_username': '@test_telegram_user'}
        auth_api_client_unverified.post(self.BASE_URL, data=data)

        assert VerificationCodeTelegram.objects.filter(telegram_username='@test_telegram_user').exists()

    def test_create_verification_code_incorrect_telegram_username(
        self,
        auth_api_client_unverified,
    ):
        """Авторизованный, но НЕверифицированный пользователь должен создать код (201 Created)."""
        data = {'telegram_username': 'test_telegram_user'}
        auth_api_client_unverified.post(self.BASE_URL, data=data, expected_status=status.HTTP_400_BAD_REQUEST)

    def test_create_verification_code_forbidden(self, auth_api_client_verified):
        """Верифицированный пользователь НЕ должен создавать код (403 Forbidden)."""
        data = {'telegram_username': '@test_telegram_user'}

        auth_api_client_verified.post(self.BASE_URL, data=data, expected_status=status.HTTP_403_FORBIDDEN)

    def test_create_verification_code_unauthorized(self, api_test_client):
        """Неавторизованный пользователь НЕ должен создавать код (401 Unauthorized)."""
        data = {'telegram_username': '@test_telegram_user'}

        api_test_client.post(self.BASE_URL, data=data, expected_status=status.HTTP_401_UNAUTHORIZED)

    # /api/v1/users/verification/verify/
    def test_verify_success(self, auth_api_client_unverified, verification_code):
        """Успешная верификация пользователя (200 OK)."""
        data = {
            'telegram_username': verification_code.telegram_username,
            'code': verification_code.code,
        }
        response = auth_api_client_unverified.post(
            self.VERIFY_URL,
            data=data,
            expected_status=status.HTTP_200_OK,
        )

        assert response == {
            'is_success': True,
            'message': 'Верификация пройдена успешно',
        }

    def test_verify_invalid_code(self, auth_api_client_unverified, verification_code):
        """Ошибка верификации: неверный код (400 Bad Request)."""
        last_digit = int(verification_code.code[-1])
        new_last_digit = (last_digit - 1) % 10
        wrong_code = verification_code.code[:-1] + str(new_last_digit)

        data = {
            'telegram_username': verification_code.telegram_username,
            'code': wrong_code,
        }
        response = auth_api_client_unverified.post(
            self.VERIFY_URL,
            data=data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )
        assert 'Неверный код верификации' in response['non_field_errors']

    def test_verify_unknown_telegram_user(self, auth_api_client_unverified, verification_code):
        """Ошибка верификации: не найден пользователь Telegram (400 Bad Request)."""
        data = {
            'telegram_username': '@unknown_user',
            'code': verification_code.code,
        }
        response = auth_api_client_unverified.post(
            self.VERIFY_URL, data=data, expected_status=status.HTTP_400_BAD_REQUEST
        )

        assert 'Не найден пользователь Telegram с таким именем.' in response['non_field_errors'][0]

    def test_verify_already_verified(self, auth_api_client_verified, verification_code):
        """Ошибка верификации: пользователь уже верифицирован (403 Forbidden)."""
        data = {
            'telegram_username': verification_code.telegram_username,
            'code': verification_code.code,
        }
        auth_api_client_verified.post(self.VERIFY_URL, data=data, expected_status=status.HTTP_403_FORBIDDEN)

    def test_verify_unauthorized(self, api_test_client, verification_code):
        """Ошибка верификации: неавторизованный пользователь (401 Unauthorized)."""
        data = {
            'telegram_username': verification_code.telegram_username,
            'code': verification_code.code,
        }
        api_test_client.post(self.VERIFY_URL, data=data, expected_status=status.HTTP_401_UNAUTHORIZED)
