from typing import Any

from django.dispatch import receiver

from apps.users.models import User

from ..models import Chat, ChatMember, Message
from ..tasks import send_ws_delete_message, send_ws_new_message
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
    send_ws_new_message.delay(
        message_id=message.id,
        chat_id=chat.id,
        user_sender_id=user_sender.id,
    )

    # TODO: добавить kafka уведомление в телегу


@receiver(last_read_message_update)
def last_read_message_callback(
    sender: Any,
    message: Message,
    chat_member: ChatMember,
    **kwargs: Any,
) -> None:
    """Обработчик сигнала обновления последнего прочитанного сообщения."""
    send_ws_delete_message.delay(message_id=message.id, user_id=chat_member.user_id)
