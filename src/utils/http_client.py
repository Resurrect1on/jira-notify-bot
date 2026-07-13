from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import httpx

from src.core.config import settings

TIMEOUT = httpx.Timeout(
    connect=settings.timeout_seconds,
    read=settings.timeout_seconds,
    write=settings.timeout_seconds,
    pool=settings.timeout_seconds,
)


@asynccontextmanager
async def async_http_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Асинхронный контекстный менеджер для отправки запросов"""

    client = httpx.AsyncClient(follow_redirects=True, timeout=TIMEOUT)

    try:
        yield client
    finally:
        await client.aclose()
