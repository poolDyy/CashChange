from decimal import Decimal

import pytest

from rest_framework import status

from apps.offers.models import Offer


@pytest.mark.django_db
class TestOfferCRUD:
    BASE_URL = '/api/v1/offers/offer/'

    def test_get_offer_list(self, api_test_client, offer, offer_rated):
        """Тест получения списка предложений."""
        response = api_test_client.get(self.BASE_URL)
        result = response['results']
        assert isinstance(result, list)
        assert result[0]['id'] == offer_rated.id
        assert result[1]['id'] == offer.id

    def test_get_offer_detail(self, api_test_client, offer):
        """Тест получения одного предложения."""
        response = api_test_client.get(f'{self.BASE_URL}{offer.id}/')
        assert response['id'] == offer.id

    def test_create_offer(self, auth_api_client_verified, offer_data):
        """Тест создания предложения."""
        response = auth_api_client_verified.post(self.BASE_URL, data=offer_data)
        created_offer = Offer.objects.get(id=response['id'])
        assert created_offer.title == offer_data['title']

    def test_create_offer_max_min_mismatch(self, auth_api_client_verified, offer_data):
        """Тест ошибки объемов."""
        offer_data['min_value'] = offer_data['max_value'] + Decimal('1.00')
        response = auth_api_client_verified.post(
            self.BASE_URL,
            data=offer_data,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

        assert 'Минимальное значение не должно превышать максимальное.' == response['min_value']

    def test_create_unverified(self, auth_api_client_unverified, offer_data):
        """Тест ошибки не верифицированного пользователя."""
        auth_api_client_unverified.post(
            self.BASE_URL,
            data=offer_data,
            expected_status=status.HTTP_403_FORBIDDEN,
        )

    def test_update_offer(self, auth_api_client_verified, offer, offer_data):
        """Тест обновления предложения."""
        new_title = 'Updated title'
        offer_data['title'] = new_title
        response = auth_api_client_verified.put(
            f'{self.BASE_URL}{offer.id}/',
            data=offer_data,
        )

        offer.refresh_from_db()
        assert offer.title == new_title
        assert response['title'] == new_title

    def test_partial_update_offer(self, auth_api_client_verified, offer):
        """Тест частичного обновления предложения."""
        new_title = 'Updated title'
        response = auth_api_client_verified.patch(
            f'{self.BASE_URL}{offer.id}/',
            data={'title': new_title},
        )

        offer.refresh_from_db()
        assert offer.title == new_title
        assert response['title'] == new_title

    def test_delete_offer(self, auth_api_client_verified, offer):
        """Тест удаления предложения."""
        auth_api_client_verified.delete(f'{self.BASE_URL}{offer.id}/')
        assert not Offer.objects.filter(id=offer.id).exists()

    def test_delete_offer_is_not_owner(self, auth_api_client_verified, offer_another_user):
        """Тест удаления предложения."""
        auth_api_client_verified.delete(
            f'{self.BASE_URL}{offer_another_user.id}/',
            expected_status=status.HTTP_403_FORBIDDEN,
        )
