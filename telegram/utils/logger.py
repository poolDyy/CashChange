import logging
import os

from logging.handlers import TimedRotatingFileHandler

from config import Config


__all__ = ['logger']


class BaseLogger:
    """Класс настройки логгера."""

    LOG_DIR = Config.LOG_DIR
    LOG_FORMAT = Config.LOG_FORMAT

    @classmethod
    def _check_log_dir(cls) -> None:
        if not os.path.exists(cls.LOG_DIR):
            os.makedirs(cls.LOG_DIR)

    @classmethod
    def setup_logger(cls) -> logging.Logger:
        """Настройка базового логгера."""
        cls._check_log_dir()
        base_logger = logging.getLogger()
        base_logger.setLevel(logging.INFO)

        formatter = logging.Formatter(cls.LOG_FORMAT)

        # Обработчик для записи в файл (все сообщения, кроме ERROR и выше)
        info_handler = TimedRotatingFileHandler(
            filename=os.path.join(cls.LOG_DIR, 'info.log'),
            when='midnight',
            interval=1,
            backupCount=1,
            encoding='utf-8',
        )
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        info_handler.addFilter(lambda record: record.levelno < logging.ERROR)

        # Обработчик для записи ошибок (ERROR и выше)
        error_handler = TimedRotatingFileHandler(
            filename=os.path.join(cls.LOG_DIR, 'error.log'),
            when='midnight',
            interval=1,
            backupCount=30,
            encoding='utf-8',
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        # Обработчик для вывода в консоль (все сообщения)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        # Добавляем обработчики в логгер
        base_logger.addHandler(info_handler)
        base_logger.addHandler(error_handler)
        base_logger.addHandler(console_handler)

        return base_logger


logger = BaseLogger.setup_logger()
