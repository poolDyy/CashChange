from telegram import KeyboardButton

__all__ = ['MainKeyBoard']

from handlers.keyboards.reply.base import BaseKeyBoard
from utils.endpoints.base import EndpointMixin


class MainKeyBoard(EndpointMixin, BaseKeyBoard):
    """Клавиатура основная."""

    KEYS = [
        KeyboardButton('Обо мне'),
    ]
    VERIFY_KEY = KeyboardButton('Верификация')

    def _get_buttons(self) -> list[KeyboardButton]:
        if self._is_user_verified():
            return self.KEYS
        return [*self.KEYS, self.VERIFY_KEY]

    def _is_user_verified(self) -> bool:
        """Проверять верифицирован ли пользователь."""

        return self.endpoints
