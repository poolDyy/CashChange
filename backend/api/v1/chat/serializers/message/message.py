from api.common.serializers import BaseSerializer
from apps.chat.models import Message

from .attachment import (
    MessageAttachmentRequestSerializer,
    MessageAttachmentResponseSerializer,
)
from .chat import MessageChatSerializer
from .users import MessageUserSerializer


__all__ = [
    'MessageRequestModelSerializer',
    'MessageResponseModelSerializer',
]


class MessageRequestModelSerializer(BaseSerializer):
    """Реквест Сериализатор сообщения."""

    attachments = MessageAttachmentRequestSerializer(many=True, required=False)

    class Meta:
        model = Message
        fields = (
            'message',
            'created_at',
            'attachments',
        )


class MessageResponseModelSerializer(BaseSerializer):
    """Респонс Сериализатор сообщения."""

    attachments = MessageAttachmentResponseSerializer(many=True, required=False)
    sender = MessageUserSerializer()
    chat = MessageChatSerializer()

    class Meta:
        model = Message
        fields = (
            'id',
            'message',
            'sender',
            'chat',
            'attachments',
        )
