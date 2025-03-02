from config import Config
from handlers import AboutHandler, StartHandler
from handlers.verify import VerifyCodeHandler
from utils.logger import logger

from telegram.ext import ApplicationBuilder


def main() -> None:
    """Инициализация бота."""
    application = ApplicationBuilder().token(Config.BOT_TOKEN).build()

    handlers = [
        StartHandler(),
        AboutHandler(),
        VerifyCodeHandler(),
    ]
    for handler in handlers:
        application.add_handler(handler.get_handler())

    if Config.IS_WEBHOOK:
        if not Config.WEBHOOK_URL:
            logger.error('WEBHOOK_URL не указан в .env файле')
            raise ValueError('WEBHOOK_URL не указан в .env файле')

        logger.info('Запуск бота в режиме Webhook')
        application.run_webhook(
            listen='0.0.0.0',
            port=Config.PORT,
            url_path='',
            webhook_url=Config.WEBHOOK_URL,
            cert=Config.CERT_PATH,
        )
    else:
        logger.info('Запуск бота в режиме Long Polling')
        application.run_polling()


if __name__ == '__main__':
    main()
