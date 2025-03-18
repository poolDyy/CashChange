import dataclasses

from datetime import datetime

from django.db import transaction
from django.utils.timezone import now

from apps.chat.models import Message
from apps.common.mixins import FromDictMixin
from apps.offers.models import Offer
from apps.users.models import User

from .. import allowed_attachment
from ..chat import ChatGetFromMembersService
from .create_service import MessageCreateService
from .dto import AttachmentDTO


__all__ = ['MessageCreateFromOfferService']


@dataclasses.dataclass
class MessageCreateFromOfferService(FromDictMixin):
    """Сервис создания сообщения из предложения."""

    sender: User
    offer: Offer
    message: str
    created_at: datetime = now()

    def create(self) -> Message:
        with transaction.atomic():
            members = User.objects.filter(id__in=[self.sender.id, self.offer.user_id]).select_for_update()
            _, chat = ChatGetFromMembersService(members=members, last_message_date=self.created_at).get_or_create()
            message = MessageCreateService(
                sender=self.sender,
                message=self.message,
                attachments=[self._get_offer_attachment()],
                chat=chat,
                created_at=self.created_at,
            ).create()
            return message

    def _get_offer_attachment(self) -> AttachmentDTO:
        return AttachmentDTO(
            attachment_name=allowed_attachment.get_model_name(Offer),
            object_id=self.offer.id,
        )
