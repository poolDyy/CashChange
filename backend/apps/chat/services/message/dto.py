from dataclasses import dataclass

from apps.common.mixins import FromDictMixin


@dataclass
class UserDTO(FromDictMixin):
    """Для создания сообщения."""

    id: int
    username: str


@dataclass
class AttachmentDTO(FromDictMixin):
    """Для создания сообщения."""

    attachment_name: str
    object_id: int
