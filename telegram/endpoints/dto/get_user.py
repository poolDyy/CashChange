import dataclasses

from endpoints.dto.base import DataBaseDTO


__all__ = [
    'RequestResponseGetUserDTO',
]


@dataclasses.dataclass
class RequestResponseGetUserDTO(DataBaseDTO):
    """Данные пользователя."""

    telegram_id: int
    telegram_username: str
    is_verified: bool
