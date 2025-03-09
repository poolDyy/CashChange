from decimal import Decimal

import pytest

from apps.geo.models import City
from apps.offers.models import Currency, Offer
from apps.telegram.models import TelegramUser
from apps.users.models import User


@pytest.fixture
def offer(mixer, verified_user) -> Offer:
    return mixer.blend(
        Offer,
        user=verified_user,
        rate=0,
        min_value=Decimal('100.00'),
        max_value=Decimal('1000.00'),
    )


@pytest.fixture
def another_telegram_user(mixer):
    return mixer.blend(TelegramUser, telegram_username='another_telegram_user', telegram_id='2222')


@pytest.fixture
def offer_another_user(mixer, another_telegram_user) -> Offer:
    user = mixer.blend(User, username='another_user', telegram_user=another_telegram_user, is_verified=True)
    return mixer.blend(
        Offer,
        user=user,
        rate=0,
        min_value=Decimal('100.00'),
        max_value=Decimal('1000.00'),
    )


@pytest.fixture
def offer_rated(mixer, verified_user) -> Offer:
    return mixer.blend(
        Offer,
        user=verified_user,
        rate=1,
        min_value=Decimal('100.00'),
        max_value=Decimal('1000.00'),
    )


@pytest.fixture
def currency(mixer) -> Currency:
    return mixer.blend(Currency)


@pytest.fixture
def offer_data(mixer) -> dict:
    city = mixer.blend(City)
    currency_ = mixer.blend(Currency)

    data = {
        'city': city.id,
        'currency': currency_.id,
        'title': 'Продам монету',
        'description': 'Срочно по выгодной цене, район Синагоги',
        'offer_type': Offer.OfferTypeChoices.SELL,
        'cost': Decimal('10.00'),
        'min_value': Decimal('100.00'),
        'max_value': Decimal('1000.00'),
    }
    return data
