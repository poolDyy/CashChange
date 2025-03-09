import pytest


@pytest.fixture
def feedback_data(mixer) -> dict:
    data = {
        'title': 'Все отлично!',
        'description': 'Все отлично! Очень удобно продавать печенье',
        'email': 'some@email.ru',
    }
    return data
