from repository import RepoMixin

__all__ = ['VerificationService']


class VerificationService(RepoMixin):
    """Сервис верификации пользователя."""

    messages = []
    is_valid = True

    def verify_telegram_code(
        self,
        *,
        code: str,
        telegram_username: str,
    ) -> bool:
        check_code = self.repo.users.verification_code_telegram.check_verification_code(
            code=code,
            telegram_username=telegram_username,
        )
        if not check_code:
            self.messages.append('Неверный код верификации')
            self.is_valid = False

        if not self.repo.telegram.telegram_user.get_telegram_user_by_user_name(telegram_username=telegram_username):
            self.messages.append(
                'Не найден пользователь Telegram с таким именем.\nУбедитесь что код был получен у Telegram-бота.'
            )
            self.is_valid = False

        return self.is_valid
