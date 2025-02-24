from repository.applications.telegram.telegram_user import TelegramUserRepo

__all__ = ['TelegramRepo']


class TelegramRepo:
    """Репозиторий приложения telegram."""

    @property
    def telegram_user(self) -> TelegramUserRepo:
        return TelegramUserRepo()
