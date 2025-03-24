from django.db import transaction

from .base import BroadcastABCService


__all__ = ['MessageCounterBroadcastService']


class MessageCounterBroadcastService(BroadcastABCService):
    """Сервис обработки событий чата в реальном времени."""

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id

    @classmethod
    def get_channel(cls, channel_id: str | int) -> str:
        return f'channel-message-counter:{channel_id}'

    def message_counter_broadcast(self, counters_data: dict) -> None:
        def _message_counter_broadcast() -> None:
            payload_data = {
                'channels': [self.get_channel(self.user_id)],
                'data': {
                    'type': 'new_message',
                    'body': counters_data,
                },
                'idempotency_key': f'message_counter_{self.user_id}',
            }
            self._broadcast(payload_data)

        transaction.on_commit(_message_counter_broadcast)
