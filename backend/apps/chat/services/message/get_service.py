from functools import cached_property

from django.db.models import QuerySet

from apps.chat.models import Chat, ChatMember, Message
from apps.chat.services.chat_member import ChatMemberUpdateLastMessageService
from apps.users.models import User
from project_selectors.chat.message import get_message_queryset_for_chat, get_new_messages, get_previous_messages


__all__ = ['MessageGetService']


class MessageGetService:
    """Класс получения сообщений."""

    MESSAGE_COUNT = 25

    def __init__(
        self,
        chat: Chat,
        user: User,
    ) -> None:
        self.chat = chat
        self.user = user

    def get_list_by_last_read(
        self,
    ) -> QuerySet[Message]:
        messages = get_message_queryset_for_chat(chat_id=self.chat.id)
        last_read_message = self.chat_member.last_read_message

        if last_read_message is None:
            return messages.order_by('-created_at')[: self.MESSAGE_COUNT]

        previous_messages = self.get_previous_massages(
            message=last_read_message,
            queryset=messages,
        )

        new_messages = self.get_new_massages(
            message=last_read_message,
            queryset=messages,
        )
        last_read_message_qs = Message.objects.filter(id=last_read_message.id)
        result = previous_messages | last_read_message_qs | new_messages
        return result.order_by('-created_at')

    def get_new_massages(
        self,
        message: Message,
        queryset: QuerySet[Message] | None = None,
    ) -> QuerySet[Message]:
        messages = get_new_messages(
            chat=self.chat,
            message=message,
            queryset=queryset,
        )[: self.MESSAGE_COUNT]

        ChatMemberUpdateLastMessageService(self.chat_member).update_last_read_message(
            message=messages[messages.count() - 1]
        )

        return messages

    def get_previous_massages(
        self,
        message: Message,
        queryset: QuerySet[Message] | None = None,
    ) -> QuerySet[Message]:
        return get_previous_messages(
            chat=self.chat,
            message=message,
            queryset=queryset,
        )[: self.MESSAGE_COUNT]

    @cached_property
    def chat_member(self) -> ChatMember:
        """"""
        return ChatMember.objects.select_related(
            'last_read_message',
        ).get(
            chat_id=self.chat.id,
            user_id=self.user.id,
        )
