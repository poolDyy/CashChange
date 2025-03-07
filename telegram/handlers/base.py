from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler


__all__ = ['BaseHandler']

from utils.logger import logger


class BaseHandler(ABC):
    """Базовый абстрактный класс для всех обработчиков."""

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Основной метод для обработки событий с обработкой ошибок."""
        try:
            await self._handle(update, context)
        except Exception as e:
            logger.error(f'Ошибка в обработчике {self.__class__.__name__}: {e}', exc_info=True)
            await update.message.reply_text('Ошибка в работе системы.')

    @abstractmethod
    async def _handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Внутренний метод для реализации логики обработки событий."""
        pass

    def get_handler(self) -> CommandHandler | MessageHandler:
        """Возвращает объект обработчика для регистрации в Application."""
        raise NotImplementedError('Метод get_handler должен быть переопределен в дочернем классе.')
