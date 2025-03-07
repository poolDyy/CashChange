from endpoints.dto import RequestCreateUserDTO, ResponseCreateUserDTO
from endpoints.endpoints.base import EndpointDTO
from utils.client.statuses import HTTP_201_CREATED

__all__ = ['CreateUserEndpoint']


class CreateUserEndpoint(EndpointDTO[RequestCreateUserDTO, ResponseCreateUserDTO]):
    """Ендпоинты создания пользователя."""

    raw_url = 'api/v1/telegram/user/'
    request_dto = RequestCreateUserDTO
    response_dto = ResponseCreateUserDTO
    success_status = HTTP_201_CREATED
