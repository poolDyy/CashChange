from handlers.base import BaseHandler
from handlers.keyboards.reply.main import MainKeyBoard
from handlers.keyboards.reply.start import StartKeyBoard
from services.telegram_user.create import CreateTelegramUserService
from utils.logger import logger

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

__all__ = ['StartHandler']


class StartHandler(BaseHandler):
    """Обработчик команды /start."""

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обрабатывает команду /start."""
        user = update.message.from_user
        user_id = user.id
        username = f'@{user.username}'

        logger.info(f'Пользователь {user_id} запустил бота.')

        service = CreateTelegramUserService(username=username, telegram_id=str(user_id))
        response = await service.create()
        if response.status == 201:
            await update.message.reply_text(
                'Рады приветствовать в нашем агрегаторе P2P.',
                reply_markup=MainKeyBoard(update=update, context=context).get_key_board(),
            )
        else:
            logger.error(
                f'Пользователь {user_id} {username} не создан:\nstatus:{response.status} \ndata:{response.data}.'
            )
            await update.message.reply_text(
                'Что-то пошло не так. Попробуй еще раз позже.',
                reply_markup=StartKeyBoard(update=update, context=context).get_key_board(),
            )

    def get_handler(self) -> CommandHandler:
        """Возвращает CommandHandler для регистрации."""
        return CommandHandler('start', self.handle)
