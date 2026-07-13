import enum
import uuid
from logging import WARNING, config, getLogger
from pathlib import Path

import structlog
from httpx import URL
from structlog.tracebacks import ExceptionDictTransformer
from structlog.types import EventDict

from src.core.config import settings
from src.core.filters import EndpointFilter
from src.utils.custom_types import HttpStr

LOG_DEFAULT_HANDLERS = ["console"]
LOG_ACCESS_HANDLERS = ["access"]
LOG_LEVEL = "DEBUG" if settings.debug else "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_IGNORE_ROUTES = ["/api/v1/core/health-check", "/api/docs/openapi.json", "/api/docs/swagger", "/api/docs/redoc"]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
        "access": {"()": "uvicorn.logging.AccessFormatter", "fmt": LOG_FORMAT},
    },
    "handlers": {
        "console": {"level": LOG_LEVEL, "class": "logging.StreamHandler", "formatter": "verbose"},
        "access": {"formatter": "access", "class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
    },
    "loggers": {
        "": {"handlers": LOG_DEFAULT_HANDLERS, "level": LOG_LEVEL},
        "uvicorn.error": {"level": LOG_LEVEL},
        "uvicorn.access": {"handlers": LOG_ACCESS_HANDLERS, "level": LOG_LEVEL, "propagate": False},
    },
}

config.dictConfig(LOGGING)
getLogger("weasyprint").setLevel(WARNING)
getLogger("fontTools.subset").setLevel(WARNING)


def stringify_values(_, __, event_dict: EventDict) -> EventDict:
    """
    Метод убирает ненужную приписку типа в логгинге.

    #### Пример:
    Строка `'request_id': UUID('cfb8ab8d-44b2-413a-b775-e712db93663b')`
    превращается в `'request_id': 'cfb8ab8d-44b2-413a-b775-e712db93663b'`
    """

    def stringify(value):
        if isinstance(value, (uuid.UUID, enum.Enum, HttpStr, URL, Path)):
            return str(value)
        return value

    return {key: stringify(val) for key, val in event_dict.items()}


def ignore_logging_routes() -> None:
    """Метод добавляет фильтры для логирования в `uvicorn.access`"""

    uvicorn_logger = getLogger("uvicorn.access")
    [uvicorn_logger.addFilter(EndpointFilter(path)) for path in LOG_IGNORE_ROUTES]


def structlog_configure() -> None:
    """Метод конфигурации для `structlog`"""

    ignore_logging_routes()

    processors = [
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.ExceptionRenderer(ExceptionDictTransformer(show_locals=True, max_frames=2)),
        stringify_values,
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )
