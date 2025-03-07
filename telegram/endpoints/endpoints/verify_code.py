from endpoints.dto import RequestVerifyCodeDTO, ResponseVerifyCodeDTO
from endpoints.endpoints.base import EndpointDTO
from utils.client.statuses import HTTP_200_OK

__all__ = ['VerifyCodeEndpoint']


class VerifyCodeEndpoint(EndpointDTO[RequestVerifyCodeDTO, ResponseVerifyCodeDTO]):
    """Ендпоинт получения кода верификации."""

    raw_url = 'api/v1/telegram/user/verification-code/'
    request_dto = RequestVerifyCodeDTO
    response_dto = ResponseVerifyCodeDTO
    success_status = HTTP_200_OK
