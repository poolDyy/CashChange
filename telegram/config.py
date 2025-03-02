import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

__all__ = ['Config']


class Config:
    """Конфигурация Бота."""

    BASE_DIR = Path(__file__).resolve().parent

    PORT = 8443

    BOT_TOKEN = os.getenv('BOT_TOKEN')

    TELEGRAM_BOT_SECRET_API_TOKEN = os.getenv('TELEGRAM_BOT_SECRET_API_TOKEN')
    BACKEND_URL = os.getenv('BACKEND_URL')

    IS_WEBHOOK = bool(int(os.getenv('IS_WEBHOOK', '0')))
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    CERT_PATH = os.getenv('CERT_PATH')

    LOG_DIR = BASE_DIR / 'logs'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
