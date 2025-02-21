FROM python:3.13.2-slim

# Настройки Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    BETTER_EXCEPTIONS=1

# Настройки pip
ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore


RUN apt update && \
    apt install --no-install-recommends -y build-essential git locales-all && \
    pip install --upgrade pip uwsgi poetry==2.1.0 && \
    poetry config virtualenvs.create false

WORKDIR /srv

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry install --no-root

COPY . /srv
RUN ./manage.py collectstatic --no-input
