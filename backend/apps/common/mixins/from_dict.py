import dataclasses

from typing import Any, Iterable, Self, get_args, get_origin


__all__ = ['FromDictMixin']


@dataclasses.dataclass
class FromDictMixin:
    """Класс миксин для датаклассов хранящий логику формирования из словаря."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        field_types = {f.name: f.type for f in dataclasses.fields(cls)}
        kwargs = {}

        for field_name, field_type in field_types.items():
            if field_name not in data:
                continue  # Пропускаем поля, которых нет в данных

            value = data[field_name]

            if dataclasses.is_dataclass(field_type):
                kwargs[field_name] = field_type.from_dict(value)
            elif (
                hasattr(field_type, '__origin__')
                and issubclass(get_origin(field_type), Iterable)
                and dataclasses.is_dataclass(get_args(field_type)[0])
            ):
                nested_dto_class = get_args(field_type)[0]
                kwargs[field_name] = [nested_dto_class.from_dict(item) for item in value]
            else:
                kwargs[field_name] = value

        return cls(**kwargs)
