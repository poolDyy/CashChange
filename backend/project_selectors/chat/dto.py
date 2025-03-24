import dataclasses

from datetime import datetime
from typing import Any


@dataclasses.dataclass
class ChatMessageCounterDTO:
    """DTO счетчика сообщений."""

    chat_id: int
    message_count: int
    last_message_text: str
    last_message_sender: str
    last_message_created: datetime

    def as_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)
