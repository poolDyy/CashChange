from utils.endpoints.endpoints.create_user import CreateUserEndpoint
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


class EndpointMixin:
    """Ендпоинты бекенд приложения."""

    @property
    def endpoints(self) -> Endpoints:
        return Endpoints()


def get_endpoints() -> Endpoints:
    """Получает ендпоинты."""
    return Endpoints()
