from api.common.serializers import BaseSerializer
from apps.chat.models import Message

from .attachment import MessageAttachmentResponseSerializer
from .chat import MessageChatSerializer
from .users import MessageUserSerializer


__all__ = [
    'MessageFromOfferRequestModelSerializer',
    'MessageFromOfferResponseModelSerializer',
]


class MessageFromOfferRequestModelSerializer(BaseSerializer):
    """Реквест Сериализатор сообщения."""

    class Meta:
        model = Message
        fields = (
            'message',
            'created_at',
        )


class MessageFromOfferResponseModelSerializer(BaseSerializer):
    """Респонс Сериализатор сообщения."""

    attachments = MessageAttachmentResponseSerializer(many=True)
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
