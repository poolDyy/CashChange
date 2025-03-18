import pytest

from rest_framework import status

from apps.chat.models import Message


@pytest.mark.django_db
class TestMessageCreate:
    BASE_URL_FROM_OFFER = '/api/v1/chat/from-offer/{}/message/'
    BASE_URL = '/api/v1/chat/{}/message/'

    @pytest.mark.parametrize(
        'url, url_object_fixture, message_data_fixture, attachment_count',
        [
            pytest.param(
                BASE_URL_FROM_OFFER,
                'offer',
                'message_data_from_offer',
                1,
                id='from_offer',
            ),
            pytest.param(
                BASE_URL,
                'chat',
                'message_data',
                2,
                id='base_url',
            ),
        ],
    )
    def test_create_message(
        self,
        request,
        # params
        url: str,
        url_object_fixture,
        message_data_fixture,
        attachment_count: int,
        #
        auth_api_client_verified,
        verified_user,
    ):
        """Тест успешного создания сообщения."""
        url_object = request.getfixturevalue(url_object_fixture)
        data_message = request.getfixturevalue(message_data_fixture)
        url = url.format(url_object.id)
        response = auth_api_client_verified.post(
            url,
            data=data_message,
        )

        message = Message.objects.filter(id=response.get('id')).first()
        assert message is not None
        assert message.message == data_message['message']
        assert message.sender == verified_user

        attachments = message.attachments.all()
        assert attachments.count() == attachment_count

    @pytest.mark.parametrize(
        'url, url_object_fixture, message_data_fixture, expected_status_code',
        [
            pytest.param(
                BASE_URL_FROM_OFFER,
                'offer',
                'message_data_from_offer',
                status.HTTP_400_BAD_REQUEST,
                id='from_offer',
            ),
            pytest.param(
                BASE_URL,
                'chat',
                'message_data',
                status.HTTP_201_CREATED,
                id='base_url',
            ),
        ],
    )
    def test_create_message_without_attachments(
        self,
        request,
        # params
        url: str,
        url_object_fixture: str,
        message_data_fixture,
        #
        expected_status_code,
        auth_api_client_verified,
    ):
        """Тест создания сообщения без вложений."""

        url_object = request.getfixturevalue(url_object_fixture)
        data_message = request.getfixturevalue(message_data_fixture)
        url = url.format(url_object.id)
        data_message['attachments'] = []
        auth_api_client_verified.post(url, data=data_message)

    @pytest.mark.parametrize(
        'url, url_object_fixture, message_data_fixture',
        [
            pytest.param(BASE_URL_FROM_OFFER, 'offer', 'message_data_from_offer', id='from_offer'),
            pytest.param(BASE_URL, 'chat', 'message_data', id='base_url'),
        ],
    )
    def test_create_message_unauthenticated(
        self,
        request,
        # params
        url: str,
        url_object_fixture: str,
        message_data_fixture,
        #
        auth_api_client_unverified,
    ):
        """Тест создания сообщения не верифицированным пользователем."""
        url_object = request.getfixturevalue(url_object_fixture)
        data_message = request.getfixturevalue(message_data_fixture)
        url = url.format(url_object.id)

        auth_api_client_unverified.post(
            url,
            data=data_message,
            expected_status=status.HTTP_403_FORBIDDEN,
        )

    @pytest.mark.parametrize(
        'url, url_object_fixture, message_data_fixture',
        [
            pytest.param(BASE_URL_FROM_OFFER, 'offer', 'message_data_from_offer', id='from_offer'),
            pytest.param(BASE_URL, 'chat', 'message_data', id='base_url'),
        ],
    )
    def test_create_message_invalid_data(
        self,
        request,
        # params
        url: str,
        url_object_fixture: str,
        message_data_fixture,
        #
        auth_api_client_verified,
    ):
        """Тест создания сообщения с неверными данными."""
        url_object = request.getfixturevalue(url_object_fixture)
        data_message = request.getfixturevalue(message_data_fixture)
        url = url.format(url_object.id)

        data_message['message'] = ''
        auth_api_client_verified.post(
            url,
            data=data_message,
            expected_status=status.HTTP_400_BAD_REQUEST,
        )
