import dataclasses

from typing import Any

import aiohttp

from config import Config
from utils.logger import logger


__all__ = [
    'ResponseData',
    'client',
]


@dataclasses.dataclass
class ResponseData:
    """Датакласс ответа от бекенда."""

    status: int
    data: dict[str, Any] = dataclasses.field(default_factory=dict)


class BackendClient:
    """Клиент для взаимодействия с бекендом."""

    BACKEND_URL = Config.BACKEND_URL
    AUTH_HEADER = {
        'X-Telegram-Bot-Token': Config.TELEGRAM_BOT_SECRET_API_TOKEN,
    }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> ResponseData:
        """
        Выполняет HTTP-запрос к бекенду.

        :param method: HTTP-метод (GET, POST и т.д.)
        :param endpoint: Конечная точка API (например, "/api/users/")
        :param data: Тело запроса (для POST)
        :param params: Параметры запроса (для GET)
        """
        url = f'{self.BACKEND_URL}{endpoint}'
        try:
            async with aiohttp.ClientSession(headers=self.AUTH_HEADER) as session:
                async with session.request(method, url, json=data, params=params) as response:
                    response_data = await response.json() if response.content_length else None
                    return ResponseData(
                        status=response.status,
                        data=response_data,
                    )
        except Exception as e:
            logger.error(
                f'Ошибка при выполнении запроса к {url}\nparams: {params}\n method:{method}\n data{data}\n {e}'
            )
            return ResponseData(status=500, data={'error': 'Ошибка приложения.'})

    async def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> ResponseData:
        """
        Выполняет GET-запрос к бекенду.

        :param endpoint: Конечная точка API (например, "/api/users/")
        :param params: Параметры запроса
        """
        return await self._make_request('GET', endpoint, params=params)

    async def post(
        self,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> ResponseData:
        """
        Выполняет POST-запрос к бекенду.

        :param endpoint: Конечная точка API (например, "/api/users/")
        :param data: Тело запроса
        """
        return await self._make_request('POST', endpoint, data=data)


client = BackendClient()
