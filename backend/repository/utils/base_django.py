from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar

from django.db.models import Model as _DjangoModel

__all__ = [
    'RepoModelDjango',
]

Model = TypeVar('Model', bound=_DjangoModel)


class RepoModelDjango(Generic[Model], ABC):
    """Базовый класс объекта репозитория Django."""

    @property
    @abstractmethod
    def model_cls(self) -> type[Model]:
        """Возвращает класс модели."""
        pass

    def create(self, **kwargs: Any) -> Model:
        """Создание записи в БД."""
        return self.model_cls.objects.create(**kwargs)

    def update(self, instance: Model, data: Dict) -> Model:
        """Метод обновления записи из БД."""
        for field, value in data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, **kwargs: Any) -> None:
        """Метод удаления записи из БД."""
        self.model_cls.objects.filter(**kwargs).delete()

    def bulk_update(self, objs: list[Model], **kwargs: Any) -> None:
        """Метод массового обновления записей в БД."""
        for obj in objs:
            for k, v in kwargs.items():
                setattr(obj, k, v)
        self.model_cls.objects.bulk_update(objs=objs, fields=kwargs.keys())  # type: ignore[attr-defined]

    def bulk_create(self, objs: list[Model], **kwargs: Any) -> None:
        """Метод массового создания записей в БД."""

        self.model_cls.objects.bulk_create(objs, **kwargs)  # type: ignore[attr-defined]

    def update_or_create(self, **kwargs: Any) -> tuple[Model, bool]:
        """Метод обновления или создания записи в БД."""
        return self.model_cls.objects.update_or_create(**kwargs)  # type: ignore[attr-defined]

    def get_or_create(self, **kwargs: Any) -> tuple[Model, bool]:
        """Метод получения или создания записи в БД."""

        return self.model_cls.objects.get_or_create(**kwargs)

    def save(self, **kwargs) -> None:
        """Метод сохранения записи в БД."""
        self.model_cls.save(**kwargs)
