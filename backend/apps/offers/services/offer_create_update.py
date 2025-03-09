import dataclasses

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Self

from rest_framework.exceptions import ValidationError

from apps.common.services.unset import UNSET, UnsetType
from apps.offers.models import Offer


if TYPE_CHECKING:
    from apps.geo.models import City
    from apps.offers.models import Currency
    from apps.users.models import User


__all__ = [
    'OfferCreateService',
    'OfferUpdateService',
]


@dataclasses.dataclass
class OfferBase(ABC):
    """Базовый класс сервиса."""

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        """Проверяет данные перед созданием."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        fields = {field.name for field in dataclasses.fields(cls)}
        filtered_data = {key: value for key, value in data.items() if key in fields}
        return cls(**filtered_data)


@dataclasses.dataclass
class OfferCreateService(OfferBase):
    """Сервис для создания предложения."""

    user: 'User'
    city: 'City'
    currency: 'Currency'
    title: str
    description: str
    offer_type: str
    cost: Decimal | None
    min_value: Decimal | None
    max_value: Decimal | None

    def validate(self) -> None:
        """Проверяет данные перед созданием."""
        if self.min_value is not None and self.max_value is not None and self.max_value < self.min_value:
            raise ValidationError(
                {
                    'min_value': 'Минимальное значение не должно превышать максимальное.',
                }
            )

    def create(self) -> 'Offer':
        """Создает новое предложение."""
        return Offer.objects.create(
            user=self.user,
            city=self.city,
            currency=self.currency,
            title=self.title,
            description=self.description,
            offer_type=self.offer_type,
            cost=self.cost,
            min_value=self.min_value,
            max_value=self.max_value,
        )


@dataclasses.dataclass
class OfferUpdateService(OfferBase):
    """Сервис для обновления предложения."""

    instance: 'Offer'
    city: 'City | UnsetType' = UNSET
    currency: 'Currency | UnsetType' = UNSET
    title: str | UnsetType = UNSET
    description: str | UnsetType = UNSET
    offer_type: str | UnsetType = UNSET
    cost: Decimal | None | UnsetType = UNSET
    min_value: Decimal | None | UnsetType = UNSET
    max_value: Decimal | None | UnsetType = UNSET

    def validate(self) -> None:
        """Проверяет данные перед обновлением."""
        min_value = self.min_value if self.min_value is not UNSET else self.instance.min_value
        max_value = self.max_value if self.max_value is not UNSET else self.instance.max_value
        if min_value is not None and max_value is not None and max_value < min_value:
            raise ValidationError(
                {
                    'min_value': 'Минимальное значение не должно превышать максимальное.',
                }
            )

    def update(self) -> 'Offer':
        """Обновляет существующее предложение."""
        offer = self.instance

        fields_to_update = [
            'city',
            'currency',
            'title',
            'description',
            'offer_type',
            'cost',
            'min_value',
            'max_value',
        ]
        for field in fields_to_update:
            value = getattr(self, field)
            if value is not UNSET:
                setattr(offer, field, value)

        offer.save()
        return offer
