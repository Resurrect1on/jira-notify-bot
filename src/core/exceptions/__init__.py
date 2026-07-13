from typing import Any

from fastapi import HTTPException, status

from src.core.constants import HTTPErrorDetail


class HTTPError(HTTPException):
    """Базовая HTTP-ошибка"""

    status_code = status.HTTP_400_BAD_REQUEST
    detail = HTTPErrorDetail.INTERNAL_ERROR_RESPONSE

    def __init__(self, headers: dict[str, Any] | None = None) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, headers=headers)


class ServiceTransportError(HTTPError):
    """Базовая транспортная ошибка для интеграционных сервисов"""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = HTTPErrorDetail.SERVICE_UNAVAILABLE


class MattermostTransportError(ServiceTransportError):
    """Транспортная ошибка при попытке взаимодействия с сервисом `Mattermost`"""

    detail = HTTPErrorDetail.MATTERMOST_UNAVAILABLE
