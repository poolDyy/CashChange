from datetime import datetime

from django.db.models import Case, Count, F, IntegerField, OuterRef, Subquery, Value, When
from django.db.models.functions import Coalesce

from apps.chat.models import Chat, ChatMember, Message
from project_selectors.chat.dto import ChatMessageCounterDTO


def get_chat_message_counters(user_id: int, chat_ids: list[int]) -> list[ChatMessageCounterDTO]:
    """Возвращает данные по новым сообщениям для нескольких чатов."""
    last_message_date_subquery = ChatMember.objects.filter(
        chat_id=OuterRef('pk'),
        user_id=user_id,
    ).values_list('last_read_message__created_at', flat=True)[:1]

    last_message_subquery = (
        Message.objects.filter(chat_id=OuterRef('pk'))
        .order_by('-created_at')
        .values(
            'created_at',
            'text',
            'sender__username',
        )[:1]
    )

    chats = (
        Chat.objects.filter(id__in=chat_ids)
        .annotate(
            last_message_date=Subquery(last_message_date_subquery),
            message_count=Count(
                Case(
                    When(
                        messages__created_at__gt=Coalesce(F('last_message_date'), datetime.min),
                        then=Value(1),
                    ),
                    output_field=IntegerField(),
                )
            ),
            last_message_text=Subquery(last_message_subquery.values('text')),
            last_message_sender=Subquery(last_message_subquery.values('sender__username')),
            last_message_created=Subquery(last_message_subquery.values('created_at')),
        )
        .values(
            'id',
            'message_count',
            'last_message_text',
            'last_message_sender',
            'last_message_created',
        )
    )
    return [
        ChatMessageCounterDTO(
            chat_id=chat['id'],
            message_count=chat.get('message_count', 0),
            last_message_text=chat['last_message_text'][:50],
            last_message_sender=chat['last_message_sender'],
            last_message_created=chat['last_message_created'],
        )
        for chat in chats
    ]
