from handlers.base import BaseHandler

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

__all__ = ['AboutHandler']

from handlers.keyboards.reply.main import MainKeyBoard


class AboutHandler(BaseHandler):
    """Обработчик сообщения Обо мне."""

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обрабатывает сообщение Обо мне."""
        await update.message.reply_text(
            'Вот что я могу сделать: ...',
            reply_markup=MainKeyBoard(update=update, context=context).get_key_board(),
        )

    def get_handler(self) -> MessageHandler:
        """Возвращает CommandHandler для регистрации."""
        return MessageHandler(filters.Text(['Обо мне']), self.handle)
