from typing import Optional, Type

from attr import dataclass
from rest_framework.serializers import Serializer


@dataclass(frozen=True)
class SerializerTypeMapping:
    """Описывает типы сериализатора."""

    response: Type[Serializer]
    request: Type[Serializer] | None = None


@dataclass(frozen=True)
class SerializerMapping:
    """Описывает структуру атрибута serializer в SerializerViewSetMixin."""

    list: Optional[SerializerTypeMapping] = None
    retrieve: Optional[SerializerTypeMapping] = None
    create: Optional[SerializerTypeMapping] = None
    update: Optional[SerializerTypeMapping] = None
    partial_update: Optional[SerializerTypeMapping] = None
    delete: Optional[SerializerTypeMapping] = None
    actions: dict[str:SerializerTypeMapping] = {}
