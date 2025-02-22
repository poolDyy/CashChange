from typing import Optional, Type

from drf_spectacular.openapi import AutoSchema
from rest_framework.serializers import Serializer

from api.common.enums import SerializerType
from api.common.views import SerializerViewSetMixin


class RequestResponseAutoSchema(AutoSchema):
    """Кастомная схема."""

    def get_request_serializer(self) -> Optional[Type[Serializer]]:
        return self._get_serializer_for_type(SerializerType.REQUEST)

    def get_response_serializers(self) -> Optional[Type[Serializer]]:
        return self._get_serializer_for_type(SerializerType.RESPONSE)

    def _get_serializer_for_type(self, serializer_type: Type[Serializer]) -> Optional[Type[Serializer]]:
        """Получает сериализатор для указанного типа или возвращает _get_serializer()."""
        if not self.view:
            return self._get_serializer()

        if issubclass(self.view.__class__, SerializerViewSetMixin):
            serializer_class = self.view.get_serializer_class(type_=serializer_type)
            return serializer_class() if serializer_class else None

        return self._get_serializer()
