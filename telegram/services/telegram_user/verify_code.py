from endpoints.endpoints import CreateUserEndpoint, GetUserEndpoint, VerifyCodeEndpoint
from endpoints.exceptions import AnswerException, Http404Exception


__all__ = ['VerifyCodeService']

from handlers.keyboards.reply.main import MainKeyBoard
from services.dto import HandlerServiceResponseDTO


class VerifyCodeService:
    """Сервис по верификации телеграм пользователя."""

    _get_user = GetUserEndpoint()
    _create_user = CreateUserEndpoint()
    _get_verify_code = VerifyCodeEndpoint()

    def __init__(self, username: str, telegram_id: int) -> None:
        self.username = username
        self.telegram_id = telegram_id

    async def verify_code(self) -> HandlerServiceResponseDTO:
        try:
            message = await self._verify_code()
        except AnswerException:
            message = 'Произошла ошибка верификации.\n Попробуйте еще раз позже.'
            return HandlerServiceResponseDTO(message=message, keyboard=MainKeyBoard)

        return HandlerServiceResponseDTO(message=message, keyboard=MainKeyBoard)

    async def _verify_code(self) -> str:
        try:
            user = await self._get_user.get(pk=self.telegram_id)
        except Http404Exception:
            user = None

        if user is None:
            user = await self._create_user.post(
                data={
                    'telegram_id': self.telegram_id,
                    'telegram_username': self.username,
                }
            )

        if user.is_verified:
            return 'Вы уже верифицированный пользователь.'

        verify_code = await self._get_verify_code.post(
            data={
                'telegram_username': user.telegram_username,
            }
        )
        return f'Ваш код подтверждения:\n{verify_code.code}'
