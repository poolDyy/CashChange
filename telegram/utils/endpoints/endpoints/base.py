from typing import Generic, Type, TypeVar

from utils.endpoints.dto.base import DataBaseDTO

__all__ = ['EndpointDTO']

T = TypeVar('T', bound=DataBaseDTO)


class EndpointDTO(Generic[T]):
    """Базовый класс ендпоинта."""

    url: str
    dto: Type[T] | None = None
