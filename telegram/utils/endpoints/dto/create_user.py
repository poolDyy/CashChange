import dataclasses

from utils.endpoints.dto.base import DataBaseDTO

__all__ = [
    'CreateUserDTO',
]


@dataclasses.dataclass
class CreateUserDTO(DataBaseDTO):
    """Данные для создания пользователя."""

    telegram_id: str
    telegram_username: str
