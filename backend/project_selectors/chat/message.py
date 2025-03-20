from django.contrib.contenttypes.prefetch import GenericPrefetch
from django.db.models import Prefetch, QuerySet

from apps.chat.models import Attachment, Chat, Message
from apps.offers.models import Offer


def get_message_queryset_for_chat(chat_id: int) -> QuerySet[Message]:
    """Возвращает сообщения для чата."""

    content_object_prefetch = GenericPrefetch(
        'attachments',
        [
            Message.objects.all(),
            Offer.objects.all(),
        ],
    )

    attachments_prefetch = Prefetch(
        'attachments',
        queryset=Attachment.objects.prefetch_related(content_object_prefetch),
    )

    return (
        Message.objects.select_related(
            'chat',
            'sender',
        )
        .prefetch_related(attachments_prefetch)
        .filter(chat_id=chat_id)
    )


def get_previous_messages(
    chat: Chat,
    message: Message,
    queryset: QuerySet[Message] | None = None,
) -> QuerySet[Message]:
    """Возвращает предыдущие сообщения."""
    messages = queryset or get_message_queryset_for_chat(chat_id=chat.id)
    return messages.filter(
        created_at__lt=message.created_at,
    ).order_by('-created_at')


def get_new_messages(
    chat: Chat,
    message: Message,
    queryset: QuerySet[Message] | None = None,
) -> QuerySet[Message]:
    """Возвращает новые сообщения."""
    messages = queryset or get_message_queryset_for_chat(chat_id=chat.id)
    return messages.filter(
        created_at__gt=message.created_at,
    ).order_by('created_at')
