import json
import uuid
from typing import Any

import uvicorn
from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.context import correlation_id
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette.middleware.sessions import SessionMiddleware
from structlog import get_logger

from src import api
from src.core.config import settings
from src.core.constants import HTTPErrorDetail
from src.core.exceptions.handlers import pydantic_validation_exc_handler, unhandled_exc_handler
from src.core.exceptions.schemas import PydanticErrorMessageSchema
from src.core.logger import structlog_configure
from src.utils.make_response import make_response

structlog_configure()
logger = get_logger()

logger.info("Trying to launch the app...", version=settings.version)
IGNORED_TRANSACTIONS = ("/api/v1/core/health-check",)

# app settings
app = FastAPI(
    title="JiraBot Notification Helper",
    # Адрес документации в красивом интерфейсе
    redoc_url="/api/docs/redoc",
    docs_url="/api/docs/swagger",
    # Адрес документации в формате OpenAPI
    openapi_url="/api/docs/openapi.json",
    version=settings.version,
    default_response_class=ORJSONResponse,
    responses={
        **make_response(422, HTTPErrorDetail.UNPROCESSABLE_ENTITY_ERROR_RESPONSE, PydanticErrorMessageSchema),
        **make_response(500, HTTPErrorDetail.INTERNAL_ERROR_RESPONSE),
    },
)

app.include_router(api.app_router)

# exception handlers
app.add_exception_handler(Exception, unhandled_exc_handler)  # type: ignore
app.add_exception_handler(RequestValidationError, pydantic_validation_exc_handler)  # type: ignore

# middlewares
app.add_middleware(
    CorrelationIdMiddleware,
    # The HTTP header key to read IDs from.
    header_name="X-Request-ID",
    # Enforce UUID formatting to limit chance of collisions
    # - Invalid header values are discarded, and an ID is generated in its place
    generator=lambda: uuid.uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a,
)
app.add_middleware(SessionMiddleware, secret_key=str(uuid.uuid4()))


@app.middleware("http")
async def session_handler_middleware(request: Request, call_next: Any) -> Any:
    response = Response(
        content=json.dumps({"detail": HTTPErrorDetail.INTERNAL_ERROR_RESPONSE}, ensure_ascii=False),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        headers={"X-Request-ID": correlation_id.get() or "", "Access-Control-Expose-Headers": "X-Request-ID"},
    )

    try:
        response = await call_next(request)
    except Exception:
        logger.error("Ошибка при выполнении запроса", request=request.url.path, exc_info=True)
    finally:
        if request.url.path not in IGNORED_TRANSACTIONS:
            logger.info(
                "Операция завершена",
                url=request.url.path,
                method=request.method,
                status_code=response.status_code,
                x_request_id=response.headers.get("X-Request-ID"),
            )

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000)
