import backoff
import httpx
from pydantic import BaseModel
from structlog import get_logger

from src.core.config import settings
from src.utils.custom_types import HttpStr
from src.utils.http_client import async_http_client

logger = get_logger()


class HttpClient:
    """Клиент для отправки `HTTP` запросов"""

    @backoff.on_exception(backoff.expo, httpx.TransportError, max_tries=settings.default_backoff_max_tries)
    async def post(self, url: str | HttpStr, obj_in: BaseModel | None = None, **kwargs) -> httpx.Response:
        """
        `POST` запрос

        Args:
            `url` (str | HttpStr): URL запроса
            `obj_in` (BaseModel | None): Pydantic модель с данными

        Returns:
            `Response`: Ответ от запроса
        """

        logger.debug("Попытка отправить POST-запрос", url=url, kwargs=f"{kwargs}")
        return await self._request("POST", url=url, obj_in=obj_in, **kwargs)

    @backoff.on_exception(backoff.expo, httpx.TransportError, max_tries=settings.default_backoff_max_tries)
    async def get(self, url: str | HttpStr, params: dict | None = None, **kwargs) -> httpx.Response:
        """
        `GET` запрос

        Args:
            `url` (str | HttpStr): URL запроса
            `params` (dict | None): Параметры запроса (query parameters)

        Returns:
            `Response`: Ответ от запроса
        """

        logger.debug("Попытка отправить GET-запрос", url=url, params=f"{params}", kwargs=f"{kwargs}")
        return await self._request("GET", url=url, params=params, **kwargs)

    @backoff.on_exception(backoff.expo, httpx.TransportError, max_tries=settings.default_backoff_max_tries)
    async def patch(self, url: str | HttpStr, obj_in: BaseModel | None = None, **kwargs) -> httpx.Response:
        """
        `PATCH` запрос

        Args:
            `url` (str | HttpStr): URL запроса
            `obj_in` (BaseModel | None): Pydantic модель с данными

        Returns:
            `Response`: Ответ от запроса
        """

        logger.debug("Попытка отправить PATCH-запрос", url=url, kwargs=f"{kwargs}")
        return await self._request("PATCH", url=url, obj_in=obj_in, **kwargs)

    @backoff.on_exception(backoff.expo, httpx.TransportError, max_tries=settings.default_backoff_max_tries)
    async def _request(
        self, method: str, url: str | HttpStr, obj_in: BaseModel | None = None, **kwargs
    ) -> httpx.Response:
        """Метод отправляет REST-API запрос с помощью библиотеки `httpx`"""

        async with async_http_client() as client:
            json_data = obj_in.model_dump(mode="json") if obj_in else None
            response = await client.request(method, url=url, json=json_data, **kwargs)
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                if httpx.codes.is_client_error(error.response.status_code):
                    logger.error(
                        "Клиентская ошибка в API-запросе", status_code=error.response.status_code, url=error.request.url
                    )
                elif httpx.codes.is_server_error(error.response.status_code):
                    logger.error(
                        "Серверная ошибка в API-запросе", status_code=error.response.status_code, url=error.request.url
                    )
                raise
            logger.debug("Успешный API запрос", method=method, url=url, kwargs=f"{kwargs}")
            return response


http_client = HttpClient()
