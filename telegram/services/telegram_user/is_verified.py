from utils.client.base import BackendClientMixin, ResponseData
from utils.client.statuses import HTTP_200_OK
from utils.endpoints.base import EndpointMixin

__all__ = ['IsVerifiedService']


class IsVerifiedService(EndpointMixin, BackendClientMixin):
    """Сервис по получению статуса верификации пользователя."""

    SUCCESS_STATUS = HTTP_200_OK

    def __init__(self, username: str) -> None:
        self.username = username

    async def is_verified(self) -> ResponseData:
        url = self.endpoints.is_verified.url
        dto = self.endpoints.is_verified.dto

        dto_instance = dto(telegram_username=self.username)

        return await self.client.post(url, data=dto_instance.as_dict())
