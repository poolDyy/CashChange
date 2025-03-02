import dataclasses

from utils.endpoints.dto.base import DataBaseDTO

__all__ = [
    'VerifyCodeDTO',
]


@dataclasses.dataclass
class VerifyCodeDTO(DataBaseDTO):
    """Данные получения кода верификации пользователя."""

    telegram_username: str
