from typing import Any

from django.dispatch import receiver

from apps.users.models import User

from ..models import Chat, Message
from ..tasks import send_ws_new_message
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
    send_ws_new_message.delay(
        message_id=message.id,
        chat_id=chat.id,
        user_sender_id=user_sender.id,
    )
