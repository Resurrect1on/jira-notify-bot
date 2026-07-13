import uuid
from collections.abc import Coroutine
from typing import Any, Callable

import structlog
from fastapi import Request, Response
from fastapi.routing import APIRoute


class ContextVarsRouterHandler(APIRoute):
    """Кастомный обработчик маршрутов для FastAPI, который добавляет контекстные переменные для логирования"""

    def get_route(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route = super().get_route_handler()

        async def custom_route(request: Request) -> Response:
            structlog.contextvars.clear_contextvars()
            structlog.contextvars.bind_contextvars(
                url=request.url.path,
                request_id=str(uuid.uuid4()),
                host=request.client.host if request.client else None,
                method=request.method,
            )

            response: Response = await original_route(request)
            return response

        return custom_route
