from typing import Any, Optional, Type

from django.db.models import Model
from rest_framework import mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from api.common.enums import SerializerType
from api.common.types import SerializerMapping


class BaseGenericViewSet(GenericViewSet):
    """Базовый ViewSet."""


class ExCreateModelMixin:
    """Создание экземпляра модели."""

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data, type_=SerializerType.REQUEST)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        serializer = self.get_serializer(instance=instance, type_=SerializerType.RESPONSE)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer: Serializer) -> Model:
        return serializer.save()


class ExUpdateModelMixin:
    """Обновление экземпляра модели."""

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data, instance=instance, type_=SerializerType.REQUEST)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_update(serializer)

        serializer = self.get_serializer(instance=instance, type_=SerializerType.RESPONSE)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def perform_update(self, serializer: Serializer) -> Model:
        return serializer.save()

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class SerializerViewSetMixin:
    """Миксин позволяющий использовать разные сериализаторы для запроса и ответа."""

    serializers: SerializerMapping

    @staticmethod
    def _none(*args: Any, **kwargs: Any) -> None:
        return None

    def get_serializer_class(self, *, type_: str = SerializerType.RESPONSE) -> Optional[Type[Serializer]]:
        action_name = getattr(self, 'action', None)
        if action_name and hasattr(self.serializers, action_name):
            serializer_mapping = getattr(self.serializers, action_name)
            if serializer_mapping and getattr(serializer_mapping, type_, None):
                return getattr(serializer_mapping, type_)
        return self._none()

    def get_serializer(self, *args: Any, **kwargs: Any) -> Serializer:
        serializer_type = kwargs.pop('type_', SerializerType.RESPONSE)
        serializer_class = self.get_serializer_class(type_=serializer_type)
        if serializer_class is None:
            raise ValueError('Serializer class not found')
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class BaseModelViewSet(
    SerializerViewSetMixin,
    ExCreateModelMixin,
    mixins.RetrieveModelMixin,
    ExUpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    Класс обеспечивает единый подход к обработке стандартных CRUD операций с дополнительной логикой
    для сериализации данных и обработки ошибок.
    """
