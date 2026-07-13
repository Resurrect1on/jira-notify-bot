from typing import Annotated

from pydantic import BaseModel, Field

from src.core.constants import Description, HTTPErrorDetail


class ErrorMessageSchema(BaseModel):
    """
    Базовая модель ошибки

    Args:
        `detail` (ErrorDetails): Более подробное описание деталей ошибки
    """

    detail: Annotated[HTTPErrorDetail, Field(description=Description.ERROR_DETAILS)]


class PydanticFieldsDetailDict(BaseModel):
    """
    Модель описания конкретной ошибки

    Args:
        `field` (str): Поле с ошибкой
        `description` (str): Описание ошибки
    """

    field: Annotated[str, Field(description=Description.FIELD)]
    description: Annotated[str, Field(description=Description.ERROR_MESSAGE)]


class PydanticErrorsDetailDict(BaseModel):
    """
    Класс для подробного описания ответа на запрос с ошибкой

    Args:
        `fields_error_details` (list[PydanticFieldsDetailDict]): Массив с ошибками
        `message` (ErrorDetails): Более подробное описание деталей ошибки
    """

    fields_error_details: Annotated[list[PydanticFieldsDetailDict], Field(description=Description.ERRORS_LIST)]
    message: Annotated[HTTPErrorDetail, Field(description=HTTPErrorDetail.UNPROCESSABLE_ENTITY_ERROR_RESPONSE)]


class PydanticErrorMessageSchema(BaseModel):
    """
    Общая модель ошибок для ответов на ошибочные запросы

    Args:
        `detail` (PydanticErrorsDetailDict): Описание всех валидационных ошибок в запросе
    """

    detail: Annotated[PydanticErrorsDetailDict, Field(description=Description.ERROR_DETAILS)]
