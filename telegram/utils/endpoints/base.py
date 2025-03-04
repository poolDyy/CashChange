from utils.endpoints.endpoints.create_user import CreateUserEndpoint
from utils.endpoints.endpoints.is_verified import IsVerifiedEndpoint
from utils.endpoints.endpoints.verify_code import VerifyCodeEndpoint

__all__ = [
    'EndpointMixin',
    'get_endpoints',
]


class Endpoints:
    """Класс содержащий все ендпоинты."""

    @property
    def create_user(self) -> CreateUserEndpoint:
        return CreateUserEndpoint()

    @property
    def verify_code(self) -> VerifyCodeEndpoint:
        return VerifyCodeEndpoint()

    @property
    def is_verified(self) -> IsVerifiedEndpoint:
        return IsVerifiedEndpoint()


class EndpointMixin:
    """Ендпоинты бекенд приложения."""

    @property
    def endpoints(self) -> Endpoints:
        return Endpoints()


def get_endpoints() -> Endpoints:
    """Получает ендпоинты."""
    return Endpoints()
