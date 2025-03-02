from repository.applications.telegram import TelegramRepo
from repository.applications.user import UsersRepo

__all__ = [
    'get_repository',
    'RepoMixin',
]


class RepoDjangoBase:
    """Класс содержащий property с репозиториями приложений."""

    @property
    def telegram(self) -> TelegramRepo:
        return TelegramRepo()

    @property
    def users(self) -> UsersRepo:
        return UsersRepo()


def get_repository() -> RepoDjangoBase:
    """Получить экземпляр репозитория."""
    return RepoDjangoBase()


class RepoMixin:
    """Репозиторий приложения."""

    @property
    def repo(self) -> RepoDjangoBase:
        return get_repository()
