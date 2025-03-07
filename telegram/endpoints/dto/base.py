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
        fields = {field.name for field in dataclasses.fields(cls)}
        filtered_data = {key: value for key, value in data.items() if key in fields}
        return cls(**filtered_data)
