from utils.client.base import BackendClientMixin, ResponseData
from utils.endpoints.base import EndpointMixin

__all__ = ['CreateTelegramUserService']


class CreateTelegramUserService(EndpointMixin, BackendClientMixin):
    """Сервис по созданию телеграм пользователя."""

    def __init__(self, username: str, telegram_id: str) -> None:
        self.username = username
        self.telegram_id = telegram_id

    async def create(self) -> ResponseData:
        url = self.endpoints.create_user.url
        dto = self.endpoints.create_user.dto

        dto_instance = dto(
            telegram_id=self.telegram_id,
            telegram_username=self.username,
        )

        return await self.client.post(url, data=dto_instance.as_dict())
