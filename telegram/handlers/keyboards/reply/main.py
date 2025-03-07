from telegram import KeyboardButton


__all__ = ['MainKeyBoard']


from .base import BaseReplyKeyBoard


class MainKeyBoard(BaseReplyKeyBoard):
    """Клавиатура основная."""

    KEYS = [
        KeyboardButton('Обо мне'),
        KeyboardButton('Верификация'),
    ]
