from typing import Generic, Type, TypeVar

from endpoints.dto.base import DataBaseDTO


__all__ = ['EndpointDTO']

from endpoints.exceptions import AnswerException, Http404Exception
from utils.client import client
from utils.client.statuses import HTTP_404_NOT_FOUND
from utils.logger import logger


Req = TypeVar('Req', bound=DataBaseDTO)
Res = TypeVar('Res', bound=DataBaseDTO)


class EndpointDTO(Generic[Req, Res]):
    """Базовый класс ендпоинта."""

    raw_url: str
    request_dto: Type[Req] | None = None
    response_dto: Type[Res] | None = None
    success_status: int

    def get_url(self, pk: int | None = None, **kwargs: dict) -> str:
        """Формирует URL с учетом вложенных параметров и идентификатора."""
        formatted_url = self.raw_url.format(**kwargs)

        if pk is not None:
            formatted_url = f'{formatted_url}{pk}/'

        return formatted_url

    async def post(self, data: dict, **kwargs: dict) -> Type[Res]:
        """Метод для выполнения POST запросов.

        Args:
            data (dict): Данные для отправки в теле запроса.
            **kwargs: Динамические параметры для формирования вложенного URL.

        Returns:
            Type[Res]: Возвращает объект ответа.
        """
        dto_instance = self.request_dto.from_dict(data)
        url = self.get_url(**kwargs)
        response = await client.post(url, data=dto_instance.as_dict())

        if response.status == self.success_status:
            return self.response_dto.from_dict(response.data)
        elif response.status == HTTP_404_NOT_FOUND:
            logger.error(f'Не найден путь\nurl: {url}\n status:{response.status}\n data:{response.data}')
            raise Http404Exception

        logger.error(f'Ошибка при отправке запроса\nurl: {url}\n status:{response.status}\n data:{response.data}')

        raise AnswerException

    async def get(self, pk: int | None = None, **kwargs: dict) -> Type[Res] | list[Res]:
        """Метод для выполнения GET запросов.

        Args:
            pk (Optional[int]): Идентификатор объекта для retrieve запроса. Если None, выполняется list запрос.
            **kwargs: Динамические параметры для формирования вложенного URL.

        Returns:
            Res | List[Res]: Возвращает либо один объект, либо список объектов.
        """
        url = self.get_url(pk=pk, **kwargs)

        response = await client.get(url)

        if response.status == self.success_status:
            if pk is not None:
                return self.response_dto.from_dict(response.data)
            else:
                return [self.response_dto.from_dict(item) for item in response.data]
        elif response.status == HTTP_404_NOT_FOUND:
            logger.error(f'Не найден путь\nurl: {url}\n status:{response.status}\n data:{response.data}')
            raise Http404Exception

        logger.error(f'Ошибка при отправке запроса\nurl: {url}\n status:{response.status}\n data:{response.data}')
        raise AnswerException
