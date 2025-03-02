from .user import UserModelRepo
from .verification_code_telegram import VerificationCodeTelegramRepo

__all__ = ['UsersRepo']


class UsersRepo:
    """Репозиторий приложения users."""

    @property
    def verification_code_telegram(self) -> VerificationCodeTelegramRepo:
        return VerificationCodeTelegramRepo()

    @property
    def user(self) -> UserModelRepo:
        return UserModelRepo()
