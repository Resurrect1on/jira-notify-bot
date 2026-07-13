# ---------- Stage 1: build dependencies ----------
FROM python:3.13-slim AS builder

# Установим нужное окружение
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Установим системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Установим Poetry
RUN pip install --upgrade pip \
    && pip install poetry

WORKDIR /app

# Скопируем только pyproject.toml и lock-файл (если есть)
COPY pyproject.toml poetry.lock* ./

# Установим зависимости
RUN poetry install --no-root --only main

# ---------- Stage 2: runtime ----------
FROM python:3.13-slim

WORKDIR /app

# Копируем установленные пакеты из builder
COPY --from=builder /usr/local /usr/local

# Копируем проект
COPY . .

# Настроим переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE 5000

# Запуск через uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]