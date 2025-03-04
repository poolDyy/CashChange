from utils.endpoints.dto import IsVerifiedDTO
from utils.endpoints.endpoints.base import EndpointDTO


class IsVerifiedEndpoint(EndpointDTO[IsVerifiedDTO]):
    """Ендпоинт для получения статуса верификации пользователя."""

    url = 'api/v1/telegram/user/is-verified/'
    dto = IsVerifiedDTO
