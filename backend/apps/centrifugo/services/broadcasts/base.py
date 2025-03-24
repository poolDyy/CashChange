import json
import logging

from abc import ABC, abstractmethod

import requests

from django.conf import settings
from requests.adapters import HTTPAdapter, Retry


class BroadcastABCService(ABC):
    """Базовый класс работы в реальном времени."""

    CENTRIFUGO_HTTP_API_KEY = settings.CENTRIFUGO_HTTP_API_KEY

    @classmethod
    @abstractmethod
    def get_channel(cls, channel_id: str | int) -> str:
        pass

    @classmethod
    def _broadcast(cls, payload_data: dict) -> None:
        session = requests.Session()
        retries = Retry(total=1, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        try:
            session.post(
                'http://centrifugo:8888/api/broadcast',
                data=json.dumps(payload_data),
                headers={
                    'Content-type': 'application/json',
                    'X-API-Key': cls.CENTRIFUGO_HTTP_API_KEY,
                    'X-Centrifugo-Error-Mode': 'transport',
                },
            )
        except requests.exceptions.RequestException as e:
            logging.error(e)
            raise
