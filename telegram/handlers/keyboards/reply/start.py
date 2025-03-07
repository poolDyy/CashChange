from telegram import KeyboardButton

__all__ = ['StartKeyBoard']

from handlers.keyboards.reply.base import BaseReplyKeyBoard


class StartKeyBoard(BaseReplyKeyBoard):
    """Клавиатура для обработчика start."""

    KEYS = [
        KeyboardButton('/start'),
    ]
