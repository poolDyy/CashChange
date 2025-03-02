from utils.endpoints.dto import VerifyCodeDTO
from utils.endpoints.endpoints.base import EndpointDTO


class VerifyCodeEndpoint(EndpointDTO[VerifyCodeDTO]):
    """Ендпоинт получения кода верификации."""

    url = 'api/v1/telegram/user/verification-code/'
    dto = VerifyCodeDTO
