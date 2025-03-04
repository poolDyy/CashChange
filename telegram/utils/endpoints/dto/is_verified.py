import dataclasses

from utils.endpoints.dto.base import DataBaseDTO

__all__ = [
    'IsVerifiedDTO',
]


@dataclasses.dataclass
class IsVerifiedDTO(DataBaseDTO):
    """Данные для получения статуса верификации пользователя."""

    telegram_username: str
