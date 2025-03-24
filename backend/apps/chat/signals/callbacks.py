from typing import Any

from django.dispatch import receiver

from api.v1.chat.serializers import MessageResponseModelSerializer
from apps.centrifugo.services.broadcasts import ChatBroadcastService, MessageCounterBroadcastService
from apps.users.models import User

from ..models import Chat, ChatMember, Message
from ..services.message import MessageCounterService
from .signals import message_create


@receiver(message_create)
def message_create_callback(
    sender: Any,
    message: Message,
    chat: Chat,
    user_sender: User,
    **kwargs: Any,
) -> None:
    """Обработчик сигнала создания сообщения."""
    message_data = MessageResponseModelSerializer(instance=message).data
    ChatBroadcastService(chat_id=chat.id).message_broadcast(message_id=message.id, message_data=message_data)

    members = ChatMember.objects.filter(
        chat_id=chat.id,
    ).exclude(
        user_id=user_sender.id,
    )
    for member in members:
        service = MessageCounterService(user=member)
        counter = service.get_for_response(chat_ids=[chat.id])
        MessageCounterBroadcastService(user_id=member.id).message_counter_broadcast(counters_data=counter)

    # TODO: разгрузить обработчик и добавить kafka уведомление в телегу