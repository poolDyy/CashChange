import dataclasses

from datetime import datetime

from django.db import transaction
from django.utils.timezone import now

from apps.chat.models import Attachment, Chat, ChatMember, Message
from apps.common.mixins import FromDictMixin
from apps.users.models import User

from .. import allowed_attachment
from .dto import AttachmentDTO


__all__ = ['MessageCreateService']

from ...signals import message_create


@dataclasses.dataclass
class MessageCreateService(FromDictMixin):
    """Сервис по созданию сообщения."""

    sender: User
    message: str
    chat: Chat
    attachments: list[AttachmentDTO] = dataclasses.field(default_factory=list)
    created_at: datetime = now()

    def __post_init__(self) -> None:
        self._filter_attachments()

    def _filter_attachments(self) -> None:
        """Фильтрует вложения, оставляя только разрешенные типы."""
        self.attachments = [
            attachment
            for attachment in self.attachments
            if attachment.attachment_name.lower() in allowed_attachment.get_allowed_models_names
        ]

    def create(self) -> Message:
        with transaction.atomic():
            message = Message.objects.create(
                chat=self.chat,
                sender=self.sender,
                message=self.message,
                created_at=self.created_at,
            )

            self._create_attachments(message=message)
            self._update_last_read_message(message=message)

        self._post_create()
        return message

    def _create_attachments(self, message: Message) -> None:
        """Создает вложения для сообщения."""
        Attachment.objects.bulk_create(
            [
                Attachment(
                    content_type=allowed_attachment.get_allowed_model_content_type_by_name(attachment.attachment_name),
                    object_id=attachment.object_id,
                    message=message,
                )
                for attachment in self.attachments
            ],
            batch_size=10,
        )

    def _update_last_read_message(self, message: Message) -> None:
        """Обновляет last_read_message для отправителя."""
        ChatMember.objects.filter(
            chat_id=self.chat.id,
            user_id=self.sender.id,
        ).update(last_read_message=message)

    def _post_create(self) -> None:
        """Метод для задач после создания сообщения."""
        message_create.send(
            sender=self.__class__,
            chat=self.chat,
            message=self.message,
            user_sender=self.sender,
        )
