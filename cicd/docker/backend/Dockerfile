# Этап 1: Сборка зависимостей и статических файлов
FROM python:3.13.2-slim as builder

# Настройки Python
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    BETTER_EXCEPTIONS=1

# Установка зависимостей для сборки
RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential && \
    pip install --upgrade pip uwsgi poetry==2.1.0 && \
    poetry config virtualenvs.create false

# Копирование файлов зависимостей
WORKDIR /srv
COPY pyproject.toml poetry.lock ./

# Установка зависимостей
RUN poetry install --no-root -vvv --no-interaction --no-cache

# Копирование проекта и сборка статических файлов
COPY . .
RUN ./manage.py collectstatic --no-input

# Этап 2: Финальный образ
FROM python:3.13.2-slim

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Копирование зависимостей и статических файлов из builder
COPY --from=builder /usr/local /usr/local
COPY --from=builder /srv/static /srv/static
COPY --from=builder /srv /srv

# Указание пути к Python-библиотекам
ENV PATH=/root/.local/bin:$PATH

WORKDIR /srv
