from handlers.base import BaseHandler
from handlers.keyboards.reply.main import MainKeyBoard
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.logger import logger


__all__ = ['StartHandler']


class StartHandler(BaseHandler):
    """Обработчик команды /start."""

    async def _handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обрабатывает команду /start."""
        user = update.message.from_user
        user_id = user.id

        logger.info(f'Пользователь {user_id} запустил бота.')

        await update.message.reply_text(
            'Рады приветствовать в нашем агрегаторе P2P.',
            reply_markup=MainKeyBoard(update=update, context=context).get_key_board(),
        )

    def get_handler(self) -> CommandHandler:
        """Возвращает CommandHandler для регистрации."""
        return CommandHandler('start', self.handle)
