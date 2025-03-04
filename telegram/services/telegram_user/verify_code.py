from utils.client.base import BackendClientMixin, ResponseData
from utils.client.statuses import HTTP_200_OK
from utils.endpoints.base import EndpointMixin

__all__ = ['VerifyCodeService']


class VerifyCodeService(EndpointMixin, BackendClientMixin):
    """Сервис по созданию телеграм пользователя."""

    SUCCESS_STATUS = HTTP_200_OK

    def __init__(self, username: str) -> None:
        self.username = username

    async def get_verify_code(self) -> ResponseData:
        url = self.endpoints.verify_code.url
        dto = self.endpoints.verify_code.dto

        dto_instance = dto(telegram_username=self.username)

        return await self.client.post(url, data=dto_instance.as_dict())
