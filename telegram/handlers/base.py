from abc import ABC, abstractmethod

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler

__all__ = ['BaseHandler']


class BaseHandler(ABC):
    """Базовый абстрактный класс для всех обработчиков."""

    @abstractmethod
    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Основной метод для обработки событий."""
        pass

    def get_handler(self) -> CommandHandler | MessageHandler:
        """Возвращает объект обработчика для регистрации в Application."""
        raise NotImplementedError('Метод get_handler должен быть переопределен в дочернем классе.')
