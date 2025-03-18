from datetime import datetime
from decimal import Decimal

import pytest

from apps.chat.models import Chat, Message
from apps.chat.services import allowed_attachment
from apps.offers.models import Currency, Offer
from apps.telegram.models import TelegramUser
from apps.users.models import User


@pytest.fixture
def telegram_user_chat(mixer):
    return mixer.blend(TelegramUser)


@pytest.fixture
def user_chat_member(mixer, telegram_user_chat):
    """Фикстура для создания пользователя."""
    return mixer.blend(User, telegram_user=telegram_user_chat, is_verified=True, is_active=True)


@pytest.fixture
def user_not_chat_member(mixer, telegram_user_chat):
    """Фикстура для создания пользователя."""
    return mixer.blend(User, telegram_user=telegram_user_chat, is_verified=True, is_active=True)


@pytest.fixture
def chat(mixer, verified_user, user_chat_member):
    """Фикстура для создания чата."""
    chat = Chat.objects.create(
        title='Test',
        last_message_date=datetime.now(),
    )
    chat.members.add(verified_user)
    chat.members.add(user_chat_member)
    return chat


@pytest.fixture
def currency(mixer):
    """Фикстура для создания валюты."""
    return mixer.blend(Currency)


@pytest.fixture
def offer(mixer, user_chat_member, currency):
    return mixer.blend(
        Offer,
        user=user_chat_member,
        currency=currency,
        rate=0,
        min_value=Decimal('100.00'),
        max_value=Decimal('1000.00'),
    )


@pytest.fixture
def message_to_attachment(mixer, user_chat_member, chat):
    """Фикстура сообщения для вложения."""
    return mixer.blend(
        Message,
        sender=user_chat_member,
        chat=chat,
    )


@pytest.fixture
def message_data(offer, message_to_attachment):
    """Фикстура для данных сообщения."""
    return {
        'message': 'Test Message',
        'attachments': [
            {
                'attachment_name': allowed_attachment.get_model_name(message_to_attachment.__class__),
                'object_id': message_to_attachment.id,
            },
            {
                'attachment_name': allowed_attachment.get_model_name(offer.__class__),
                'object_id': offer.id,
            },
        ],
    }


@pytest.fixture
def message_data_from_offer():
    """Фикстура для данных сообщения."""
    return {
        'message': 'Test Message from offer',
    }
