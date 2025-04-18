from apps.chat.models import ChatMember, Message


__all__ = ['ChatMemberUpdateLastMessageService']


class ChatMemberUpdateLastMessageService:
    """Класс обновляющий последнее прочитанное сообщение."""

    def __init__(self, chat_member: ChatMember) -> None:
        self.chat_member = chat_member

    def _is_message_new(self, message: Message) -> bool:
        return self.chat_member.last_read_message.created_at < message.created_at

    def update_last_read_message(self, message: Message) -> None:
        if self._is_message_new(message=message):
            self.chat_member.last_read_message = message
            self.chat_member.save()
