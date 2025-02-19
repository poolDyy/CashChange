import pytest
from mixer.backend.django import mixer as _mixer

from .common import ApiTestClient


@pytest.fixture(scope='session')
def api_client():
    return ApiTestClient()


@pytest.fixture(scope='session')
def mixer():
    return _mixer
