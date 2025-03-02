FROM python:3.13.2-slim as builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential && \
    pip install --upgrade pip poetry==2.1.0 && \
    poetry config virtualenvs.create false

WORKDIR /srv
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root -vvv --no-interaction --no-cache

COPY . .

FROM python:3.13.2-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /usr/local /usr/local
COPY --from=builder /srv /srv

ENV PATH=/root/.local/bin:$PATH

RUN mkdir -p /srv/logs

WORKDIR /srv

