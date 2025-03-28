from django.db import transaction

from .base import BroadcastABCService


__all__ = ['UserBroadcastService']


class UserBroadcastService(BroadcastABCService):
    """Сервис обработки событий чата в реальном времени."""

    def __init__(self, users_id: list[int]) -> None:
        self.users_id = users_id

    @classmethod
    def get_channel(cls, channel_id: str | int) -> str:
        return f'user:{channel_id}'

    def new_message_broadcast(self, message_id: int, message_data: dict) -> None:
        def _message_counter_broadcast() -> None:
            payload_data = {
                'channels': [self.get_channel(user_id) for user_id in self.users_id],
                'data': {
                    'type': 'new_message',
                    'body': message_data,
                },
                'idempotency_key': f'new_message_{message_id}',
            }
            self._broadcast(payload_data)

        transaction.on_commit(_message_counter_broadcast)

    def update_last_read_message_broadcast(self, message_id: int, data: dict) -> None:
        def _update_last_read_message_broadcast() -> None:
            payload_data = {
                'channels': [self.get_channel(user_id) for user_id in self.users_id],
                'data': {
                    'type': 'update_last_read_message',
                    'body': data,
                },
                'idempotency_key': f'update_last_read_message_{message_id}',
            }
            self._broadcast(payload_data)

        transaction.on_commit(_update_last_read_message_broadcast)
