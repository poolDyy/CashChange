from celery import shared_task

from api.v1.chat.serializers import MessageResponseModelSerializer
from apps.centrifugo.services.broadcasts import UserBroadcastService
from apps.chat.models import ChatMember, Message


@shared_task(queue='ws')
def send_ws_new_message(
    message_id: int,
    chat_id: int,
    user_sender_id: int,
) -> None:
    """Отправка нового сообщения."""
    message = Message.objects.get(id=message_id)
    message_data = MessageResponseModelSerializer(instance=message).data
    users_id = (
        ChatMember.objects.filter(
            chat_id=chat_id,
        )
        .exclude(
            user_id=user_sender_id,
        )
        .values_list('user_id', flat=True)
    )
    UserBroadcastService(users_id=users_id).new_message_broadcast(
        message_id=message_id,
        message_data=message_data,
    )
