__all__ = ['VerificationService']

from typing import TYPE_CHECKING

from apps.telegram.models import TelegramUser
from apps.users.models import VerificationCodeTelegram

if TYPE_CHECKING:
    from apps.users.models import User


class CodeDoesNotValid(Exception):
    """Ошибка указывающая на быстрый выход из функции verify класса VerificationService."""

    pass


class VerificationService:
    """Сервис верификации пользователя."""

    def __init__(self) -> None:
        self.errors = []
        self.is_valid = True

    def verify(self, code: str, telegram_username: str, user: 'User') -> None:
        try:
            telegram_user = self._get_telegram_user_by_user_name(telegram_username=telegram_username)

            self._check_verification_code(
                code=code,
                telegram_username=telegram_username,
            )

            user.telegram_user = telegram_user
            user.is_verified = True
            user.save()
        except CodeDoesNotValid:
            return

    def _get_telegram_user_by_user_name(self, telegram_username: str) -> TelegramUser | None:
        try:
            return TelegramUser.objects.get(telegram_username=telegram_username)
        except TelegramUser.DoesNotExist:
            self.errors.append(
                'Не найден пользователь Telegram с таким именем.\nУбедитесь что код был получен у Telegram-бота.'
            )
            self.is_valid = False
            raise CodeDoesNotValid

    def _check_verification_code(self, code: str, telegram_username: str) -> None:
        check_code = VerificationCodeTelegram.objects.filter(
            code=code,
            telegram_username=telegram_username,
        ).exists()
        if not check_code:
            self.errors.append('Неверный код верификации')
            self.is_valid = False
            raise CodeDoesNotValid
