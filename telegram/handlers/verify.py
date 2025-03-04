from handlers.base import BaseHandler
from handlers.keyboards.reply.main import MainKeyBoard
from services.telegram_user.create import CreateTelegramUserService
from services.telegram_user.verify_code import VerifyCodeService
from utils.logger import logger

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

__all__ = ['VerifyCodeHandler']


class VerifyCodeHandler(BaseHandler):
    """Обработчик команды /start."""

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обрабатывает сообщение Верификация."""
        user = update.message.from_user

        logger.info(f'Пользователь {user.id} запросил код верификации.')
        await self.create_telegram_user(update, context)
        await self.get_verify_code(update, context)

    async def get_verify_code(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.message.from_user
        service = VerifyCodeService(username=user.username)
        response = await service.get_verify_code()

        if response.status == 200:
            await update.message.reply_text(
                f'Код верификации:\n{response.data.get("code")}',
                reply_markup=MainKeyBoard(update=update, context=context).get_key_board(),
            )
        else:
            logger.error(
                f'Пользователь {user.id} не получил код верификации:\nstatus:{response.status} \ndata:{response.data}.'
            )
            await update.message.reply_text(
                'Что-то пошло не так. Попробуй еще раз позже.',
                reply_markup=MainKeyBoard(update=update, context=context).get_key_board(),
            )

    async def create_telegram_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.message.from_user
        service = CreateTelegramUserService(username=user.username, telegram_id=str(user.id))
        response = await service.create()
        if response.status == 201:
            await update.message.reply_text(
                'Рады приветствовать в нашем агрегаторе P2P.',
                reply_markup=MainKeyBoard(update=update, context=context).get_key_board(),
            )
        else:
            logger.error(
                f'Пользователь {user.id} {user.username} не создан:\nstatus:{response.status} \ndata:{response.data}.'
            )
            await update.message.reply_text(
                'Что-то пошло не так. Попробуй еще раз позже.',
                reply_markup=MainKeyBoard(update=update, context=context).get_key_board(),
            )

    def get_handler(self) -> MessageHandler:
        """Возвращает CommandHandler для регистрации."""
        return MessageHandler(filters.Text(['Верификация']), self.handle)
