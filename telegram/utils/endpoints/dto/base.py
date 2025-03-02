import dataclasses
from abc import ABC
from typing import Any, Self

__all__ = [
    'DataBaseDTO',
]


@dataclasses.dataclass
class DataBaseDTO(ABC):
    """Базовый класс для данных ендпоинта."""

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(**data)
