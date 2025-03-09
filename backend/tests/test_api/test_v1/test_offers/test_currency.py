import pytest


@pytest.mark.django_db
class TestCurrency:
    BASE_URL = '/api/v1/offers/currency/'

    def test_get_currency_list(self, api_test_client, currency):
        """Тест получения списка предложений."""
        response = api_test_client.get(self.BASE_URL)
        result = response['results']
        assert isinstance(result, list)
        assert result[0]['id'] == currency.id
