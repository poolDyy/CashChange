from django.contrib.contenttypes.prefetch import GenericPrefetch
from django.db.models import Prefetch, QuerySet

from apps.chat.models import Attachment, Message
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
