import dataclasses

from endpoints.dto.base import DataBaseDTO

__all__ = [
    'RequestVerifyCodeDTO',
    'ResponseVerifyCodeDTO',
]


@dataclasses.dataclass
class RequestVerifyCodeDTO(DataBaseDTO):
    """Данные получения кода верификации пользователя."""

    telegram_username: str


@dataclasses.dataclass
class ResponseVerifyCodeDTO(DataBaseDTO):
    """Данные получения кода верификации пользователя."""

    code: str
