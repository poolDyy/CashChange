from apps.users.models import VerificationCodeTelegram
from apps.users.services.user_verification import VerificationCodeCreateService
from repository.utils.base_django import RepoModelDjango

__all__ = ['VerificationCodeTelegramRepo']


class VerificationCodeTelegramRepo(RepoModelDjango[VerificationCodeTelegram]):
    """Репозиторий для работы с кодом верификации."""

    @property
    def model_cls(self) -> type[VerificationCodeTelegram]:
        return VerificationCodeTelegram

    def create(self, *, telegram_username: str) -> VerificationCodeTelegram:
        return VerificationCodeCreateService.create_verification_code(telegram_username=telegram_username)

    def check_verification_code(self, *, code: str, telegram_username: str) -> bool:
        return self.model_cls.objects.filter(
            code=code,
            telegram_username=telegram_username,
        ).exists()

    def get_first_by_telegram_username(self, *, telegram_username: str) -> VerificationCodeTelegram:
        return self.model_cls.objects.filter(
            telegram_username=telegram_username,
        ).first()
