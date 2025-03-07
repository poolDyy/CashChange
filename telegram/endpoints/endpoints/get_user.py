from endpoints.dto import RequestResponseGetUserDTO
from endpoints.endpoints.base import EndpointDTO
from utils.client.statuses import HTTP_200_OK

__all__ = ['GetUserEndpoint']


class GetUserEndpoint(EndpointDTO[None, RequestResponseGetUserDTO]):
    """Ендпоинт получения пользователя."""

    raw_url = 'api/v1/telegram/user/'
    request_dto = None
    response_dto = RequestResponseGetUserDTO
    success_status = HTTP_200_OK
