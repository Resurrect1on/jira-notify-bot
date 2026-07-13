from asgi_correlation_id import correlation_id
from fastapi import HTTPException, Request, Response, status
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from structlog import get_logger

from src.core.constants import HTTPErrorDetail

logger = get_logger()


async def unhandled_exc_handler(request: Request) -> ORJSONResponse | Response:
    return await http_exception_handler(
        request,
        HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=HTTPErrorDetail.INTERNAL_ERROR_RESPONSE,
            headers={"X-Request-ID": correlation_id.get() or "", "Access-Control-Expose-Headers": "X-Request-ID"},
        ),
    )


async def pydantic_validation_exc_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse | Response:
    details = exc.errors()
    errors_list = []

    for error in details:
        error_msg = error.get("msg", HTTPErrorDetail.UNKNOWN_ERROR_RESPONSE)
        if error.get("type") == "json_invalid":
            return await http_exception_handler(
                request,
                HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail={
                        "message": HTTPErrorDetail.UNPROCESSABLE_ENTITY_ERROR_RESPONSE,
                        "fields_error_details": [{"field": "json", "description": error_msg}],
                    },
                ),
            )
        else:
            location = error.get("loc", ["Unknown field"])
            errors_list.append({"field": location[-1], "description": error_msg})

    return await http_exception_handler(
        request,
        HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail={
                "message": HTTPErrorDetail.UNPROCESSABLE_ENTITY_ERROR_RESPONSE,
                "fields_error_details": errors_list,
            },
        ),
    )
