from rest_framework import serializers

from api.common.serializers import BaseSerializer
from apps.chat.models import Attachment, Message
from apps.chat.services import allowed_attachment
from apps.offers.models import Offer


__all__ = [
    'MessageAttachmentResponseSerializer',
    'MessageAttachmentRequestSerializer',
]


class AttachmentMessageModelSerializer(BaseSerializer):
    """Сериализатор сообщения как вложение."""

    class Meta:
        model = Message
        fields = (
            'id',
            'message',
            'sender',
            'created_at',
        )


class AttachmentOfferModelSerializer(BaseSerializer):
    """Сериализатор предложения как вложение."""

    currency = serializers.CharField(source='currency.code', read_only=True)

    class Meta:
        model = Offer
        fields = (
            'id',
            'title',
            'description',
            'currency',
            'cost',
        )


class MessageAttachmentResponseSerializer(serializers.ModelSerializer):
    """Сериализатор вложений сообщения."""

    OBJECT_SERIALIZER_MAPPING = {
        allowed_attachment.get_model_name(Message): AttachmentMessageModelSerializer,
        allowed_attachment.get_model_name(Offer): AttachmentOfferModelSerializer,
    }

    content_object = serializers.SerializerMethodField()
    attachment_name = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = (
            'id',
            'attachment_name',
            'content_object',
        )

    def get_content_object(self, instance: Attachment) -> dict | None:
        content_instance = instance.content_object
        model_name = allowed_attachment.get_model_name(content_instance.__class__)

        serializer = self.OBJECT_SERIALIZER_MAPPING.get(model_name)
        if serializer:
            return serializer(instance=content_instance).data

    def get_attachment_name(self, instance: Attachment) -> str:
        return allowed_attachment.get_model_name(instance.content_object.__class__)


class MessageAttachmentRequestSerializer(serializers.ModelSerializer):
    """Сериализатор вложений сообщения."""

    attachment_name = serializers.CharField(max_length=255)

    class Meta:
        model = Attachment
        fields = (
            'id',
            'object_id',
            'attachment_name',
        )
