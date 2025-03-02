from telegram import KeyboardButton

__all__ = ['StartKeyBoard']

from handlers.keyboards.reply.base import BaseKeyBoard


class StartKeyBoard(BaseKeyBoard):
    """Клавиатура для обработчика start."""

    KEYS = [
        KeyboardButton('/start'),
    ]
