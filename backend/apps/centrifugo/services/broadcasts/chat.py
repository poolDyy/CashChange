from django.db import transaction

from .base import BroadcastABCService


__all__ = ['ChatBroadcastService']


class ChatBroadcastService(BroadcastABCService):
    """Сервис обработки событий чата в реальном времени."""

    def __init__(self, chat_id: int) -> None:
        self.chat_id = chat_id

    @classmethod
    def get_channel(cls, channel_id: str | int) -> str:
        return f'channel-chat:{channel_id}'

    def message_broadcast(self, message_id: int, message_data: dict) -> None:
        def _message_broadcast() -> None:
            payload_data = {
                'channels': [self.get_channel(self.chat_id)],
                'data': {
                    'type': 'new_message',
                    'body': message_data,
                },
                'idempotency_key': f'chat_{self.chat_id}_message_{message_id}',
            }
            self._broadcast(payload_data)

        transaction.on_commit(_message_broadcast)
