from functools import cached_property

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model

from apps.chat.models import Message
from apps.common.metaclasses import SingletonMeta
from apps.offers.models import Offer


__all__ = [
    'AllowedAttachment',
    'allowed_attachment',
]


class AllowedAttachment(metaclass=SingletonMeta):
    """Класс содержащий информацию и методы по разрешенным вложениям сообщений.

    При добавлении новых моделей необходимо создать сериализатор по пути api/v*/chat/serializers/message/attachment.py
    """

    ALLOWED_ATTACHMENTS_MODELS = [
        Message,
        Offer,
    ]

    ALLOWED_ATTACHMENT_TYPE = Message | Offer

    @cached_property
    def content_type_map(self) -> dict[str, ContentType]:
        return {self.get_model_name(m): ContentType.objects.get_for_model(m) for m in self.ALLOWED_ATTACHMENTS_MODELS}

    @property
    def get_allowed_models_names(self) -> list[str]:
        return [self.get_model_name(m) for m in self.ALLOWED_ATTACHMENTS_MODELS]

    @classmethod
    def get_model_name(cls, django_model: type[Model]) -> str:
        return django_model.__name__.lower()

    def get_allowed_model_content_type(self, django_model: type[Model]) -> ContentType:
        return self.content_type_map.get(self.get_model_name(django_model))

    def get_allowed_model_content_type_by_name(self, django_model_name: str) -> ContentType:
        return self.content_type_map.get(django_model_name)


allowed_attachment = AllowedAttachment()
