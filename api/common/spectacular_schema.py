from rest_framework.schemas import AutoSchema

from api.common.enums import SerializerType
from api.common.views import SerializerViewSetMixin


class RequestResponseAutoSchema(AutoSchema):
    """Кастомная схема."""

    def get_request_serializer(self) -> None:
        if issubclass(self.view, SerializerViewSetMixin):
            return self.view.get_serializer_class(type_=SerializerType.REQUEST)()
        return self._get_serializer()

    def get_response_serializers(self) -> None:
        if issubclass(self.view, SerializerViewSetMixin):
            return self.view.get_serializer_class(type_=SerializerType.RESPONSE)()
        return self._get_serializer()
