import dataclasses
from typing import Type

from handlers.keyboards.reply.base import BaseReplyKeyBoard

__all__ = ['HandlerServiceResponseDTO']


@dataclasses.dataclass
class HandlerServiceResponseDTO:
    """Структура ответа сервисов для обработчиков."""

    message: str
    keyboard: Type[BaseReplyKeyBoard]
