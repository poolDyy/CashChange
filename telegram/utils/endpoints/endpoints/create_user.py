from utils.endpoints.dto import CreateUserDTO
from utils.endpoints.endpoints.base import EndpointDTO


class CreateUserEndpoint(EndpointDTO[CreateUserDTO]):
    """Ендпоинты создания пользователя."""

    url = 'api/v1/telegram/user/'
    dto = CreateUserDTO
