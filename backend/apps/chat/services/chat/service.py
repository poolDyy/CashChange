from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

from django.db.models import Q
from django.utils.timezone import now

from apps.chat.models import Chat
from apps.common.mixins import FromDictMixin


if TYPE_CHECKING:
    from apps.users.models import User


__all__ = [
    'ChatCreateService',
    'ChatGetFromMembersService',
]


@dataclass
class ChatCreateService(FromDictMixin):
    """Сервис по созданию чата."""

    members: 'list[User]'
    last_message_date: datetime = now()
    title: str | None = None

    def __post_init__(self) -> None:
        if self.title is None:
            self.title = ', '.join([member.username for member in self.members])[:255]

    def create(self) -> Chat:
        instance = Chat.objects.create(
            title=self.title,
            last_message_date=self.last_message_date,
        )
        instance.members.set(
            self.members,
            through_defaults={'created_at': self.last_message_date},
        )
        return instance


@dataclass
class ChatGetFromMembersService(FromDictMixin):
    """Класс для получения чата по его участникам."""

    members: 'list[User]'
    last_message_date: datetime = now()

    def get_or_create(self) -> tuple[bool, Chat]:
        query = Q()
        for member in self.members:
            query &= Q(members=member)

        chat = Chat.objects.filter(query).first()

        if chat is None:
            return False, ChatCreateService(
                members=self.members,
                last_message_date=self.last_message_date,
            ).create()

        return True, chat
