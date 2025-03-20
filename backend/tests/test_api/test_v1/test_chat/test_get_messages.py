import pytest

from rest_framework import status

from apps.chat.services.message import MessageGetService


@pytest.mark.django_db
class TestGetMessages:
    BASE_URL = '/api/v1/chat/{}/message/'
    BASE_URL_PREVIOUS = BASE_URL + 'previous-messages/{}/'
    BASE_URL_NEW = BASE_URL + 'new-messages/{}/'

    def test_list_messages(self, auth_api_client_verified, messages_list, chat):
        url = self.BASE_URL.format(chat.id)
        response = auth_api_client_verified.get(url)

        assert len(response) == MessageGetService.MESSAGE_COUNT * 2 + 1
        assert response[-1]['id'] > messages_list[0].id  # проверяет что не возвращает сразу все старые сообщения
        assert response[0]['id'] < messages_list[-1].id  # проверяет что не возвращает сразу все новые сообщения
        assert all(
            [response[index]['created_at'] > response[index + 1]['created_at'] for index in range(len(response) - 1)]
        )

    def test_perms(self, auth_api_client_verified, messages_list, chat_without_user):
        url = self.BASE_URL.format(chat_without_user.id)
        auth_api_client_verified.get(url, expected_status=status.HTTP_403_FORBIDDEN)

    def test_get_previous_message(self, auth_api_client_verified, messages_list, chat):
        url = self.BASE_URL_PREVIOUS.format(chat.id, messages_list[6].id)
        response = auth_api_client_verified.get(url)
        assert len(response) == 6

    def test_get_new_message(self, auth_api_client_verified, messages_list, chat):
        mes_id = messages_list[-5].id
        url = self.BASE_URL_NEW.format(chat.id, mes_id)
        response = auth_api_client_verified.get(url)
        assert len(response) == 4
