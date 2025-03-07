import dataclasses

from endpoints.dto.base import DataBaseDTO

__all__ = [
    'ResponseCreateUserDTO',
    'RequestCreateUserDTO',
]


@dataclasses.dataclass
class RequestCreateUserDTO(DataBaseDTO):
    """Данные для создания пользователя."""

    telegram_id: int
    telegram_username: str


@dataclasses.dataclass
class ResponseCreateUserDTO(DataBaseDTO):
    """Данные для создания пользователя."""

    telegram_id: int
    telegram_username: str
    is_verified: bool
