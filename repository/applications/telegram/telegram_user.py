from apps.telegram.models import TelegramUser
from repository.utils.base_django import RepoModelDjango

__all__ = ['TelegramUserRepo']


class TelegramUserRepo(RepoModelDjango[TelegramUser]):
    """Репозиторий для работы с пользователями телеграм."""

    @property
    def model_cls(self) -> type[TelegramUser]:
        return TelegramUser

    def get_telegram_user_by_user_name(self, *, telegram_username: str) -> TelegramUser | None:
        try:
            return self.model_cls.objects.get(telegram_username=telegram_username)
        except self.model_cls.DoesNotExist:
            return None
