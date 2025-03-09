import pytest

from rest_framework import status


@pytest.mark.django_db
class TestCurrency:
    BASE_URL = '/api/v1/feedback/'

    def test_create_feedback(self, auth_api_client_verified, feedback_data):
        """Тест получения списка предложений."""
        auth_api_client_verified.post(self.BASE_URL, data=feedback_data)

    def test_create_feedback_unverified(self, auth_api_client_unverified, feedback_data):
        """Тест получения списка предложений."""
        auth_api_client_unverified.post(self.BASE_URL, data=feedback_data, expected_status=status.HTTP_403_FORBIDDEN)
