__all__ = [
    'get_repository',
    'RepoMixin',
]


class RepoDjangoBase:
    """Класс содержащий property с репозиториями приложений."""


def get_repository() -> RepoDjangoBase:
    """Получить экземпляр репозитория."""
    return RepoDjangoBase()


class RepoMixin:
    """Репозиторий приложения."""

    @property
    def repo(self) -> RepoDjangoBase:
        return get_repository()
