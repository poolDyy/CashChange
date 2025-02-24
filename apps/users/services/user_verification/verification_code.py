from random import randint

from apps.users.models import VerificationCodeTelegram

__all__ = ['VerificationCodeCreateService']


class VerificationCodeCreateService:
    """Класс создания кода верификации. Используется в репозитории."""

    model = VerificationCodeTelegram

    @classmethod
    def _generate_verification_code(cls, *, telegram_username: str) -> str:
        code = str(randint(100000, 999999))
        if cls.model.objects.filter(code=code, telegram_username=telegram_username).exists():
            return cls._generate_verification_code(telegram_username=telegram_username)
        return code

    @classmethod
    def create_verification_code(cls, *, telegram_username: str) -> VerificationCodeTelegram:
        return cls.model.objects.create(
            telegram_username=telegram_username,
            code=cls._generate_verification_code(telegram_username=telegram_username),
        )
