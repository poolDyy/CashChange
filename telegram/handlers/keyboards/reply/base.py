from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import CallbackContext


class BaseKeyBoard:
    """Базовый класс клавиатуры."""

    KEYS = []

    def __init__(self, update: Update, context: CallbackContext) -> None:
        self.update = update
        self.context = context

    def _get_buttons(self) -> list[KeyboardButton]:
        return self.KEYS

    def get_key_board(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup.from_column(self._get_buttons())
