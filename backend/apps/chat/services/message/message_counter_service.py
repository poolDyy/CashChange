from typing import TYPE_CHECKING

from apps.chat.models import ChatMember
from apps.users.models import User
from project_selectors.chat.chat import get_chat_message_counters


if TYPE_CHECKING:
    from project_selectors.chat.dto import ChatMessageCounterDTO


class MessageCounterService:
    """Счетчик новых сообщений."""

    def __init__(self, user: User) -> None:
        self.user = user

    def get_for_response(self, chat_ids: list[int] | None = None) -> dict[int, dict]:
        """Вовзраващает счетчики для респонса."""
        counters = self.get_chats_new_message_counts(chat_ids)
        return {counter.chat_id: counter.as_dict() for counter in counters}

    def get_chats_new_message_counts(self, chat_ids: list[int] | None = None) -> 'list[ChatMessageCounterDTO]':
        """Возвращает данные по новым сообщениям для нескольких чатов."""
        if chat_ids is None:
            chat_ids = ChatMember.objects.filter(user=self.user).values_list('chat_id', flat=True)

        result = get_chat_message_counters(user_id=self.user.id, chat_ids=chat_ids)
        return result
