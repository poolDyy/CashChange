from handlers.base import BaseHandler
from services.telegram_user.verify_code import VerifyCodeService
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from utils.logger import logger


__all__ = ['VerifyCodeHandler']


class VerifyCodeHandler(BaseHandler):
    """Обработчик команды /start."""

    async def _handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обрабатывает сообщение Верификация."""
        user = update.message.from_user

        logger.info(f'Пользователь {user.id} запросил код верификации.')
        service = VerifyCodeService(username=user.username, telegram_id=user.id)
        response = await service.verify_code()
        await update.message.reply_text(
            text=response.message,
            reply_markup=response.keyboard(update=update, context=context).get_key_board(),
        )

    def get_handler(self) -> MessageHandler:
        """Возвращает CommandHandler для регистрации."""
        return MessageHandler(filters.Text(['Верификация']), self.handle)
