from apps.users.models import User
from repository.utils.base_django import RepoModelDjango

__all__ = ['UserModelRepo']


class UserModelRepo(RepoModelDjango[User]):
    """Репозиторий для работы с пользователем."""

    @property
    def model_cls(self) -> type[User]:
        return User

    def create(self, *, username: str, name: str, password: str) -> User:
        return User.objects.create_user(username=username, name=name, password=password)

    def is_verified_by_telegram_username(self, *, telegram_username: str) -> bool:
        user = self.model_cls.objects.filter(telegram_user__telegram_username=telegram_username).first()
        if user is None:
            return False
        return user.is_verified

    @classmethod
    def add_telegram_user_to_user(cls, *, telegram_username: str, user: User) -> None:
        from repository import get_repository

        repo = get_repository()

        telegram_user = repo.telegram.telegram_user.get_telegram_user_by_user_name(
            telegram_username=telegram_username,
        )

        if telegram_user:
            user.telegram_user = telegram_user
            user.save()
            return

        raise ValueError('Telegram пользователь не найден.')
