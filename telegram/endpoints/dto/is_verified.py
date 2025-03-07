import dataclasses

from endpoints.dto.base import DataBaseDTO

__all__ = [
    'RequestIsVerifiedDTO',
    'ResponseIsVerifiedDTO',
]


@dataclasses.dataclass
class RequestIsVerifiedDTO(DataBaseDTO):
    """Данные для получения статуса верификации пользователя."""

    telegram_username: str


@dataclasses.dataclass
class ResponseIsVerifiedDTO(DataBaseDTO):
    """Данные ответа о статусе верификации пользователя."""

    is_verified: bool
