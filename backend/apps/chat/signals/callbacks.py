from typing import Any

from django.dispatch import receiver

from api.v1.chat.serializers import MessageResponseModelSerializer
from apps.users.models import User

from ...centrifugo.services.broadcasts import UserBroadcastService
from ..models import Chat, ChatMember, Message
from .signals import last_read_message_update, message_create


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
    users_id = (
        ChatMember.objects.filter(
            chat_id=chat.id,
        )
        .exclude(
            user_id=user_sender.id,
        )
        .values_list('user_id', flat=True)
    )
    UserBroadcastService(users_id=users_id).new_message_broadcast(
        message_id=message.id,
        message_data=message_data,
    )
    # TODO: добавить kafka уведомление в телегу перписать на ассинхронное


@receiver(last_read_message_update)
def last_read_message_callback(
    sender: Any,
    message: Message,
    chat_member: ChatMember,
    **kwargs: Any,
) -> None:
    """Обработчик сигнала обновления последнего прочитанного сообщения."""
    data = {
        'id': message.id,
        'created_at': message.created_at,
    }
    UserBroadcastService(users_id=[chat_member.user_id]).update_last_read_message_broadcast(
        message_id=message.id,
        data=data,
    )
    # todo  перписать на ассинхронное
