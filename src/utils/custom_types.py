from typing import Annotated, Any, TypeVar

from pydantic import AnyHttpUrl, BaseModel, BeforeValidator
from pydantic_core import PydanticCustomError, core_schema

StrippedStr = Annotated[str, BeforeValidator(lambda v: v.strip() if isinstance(v, str) else v)]
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class HttpStr(str):
    """Класс для валидации ссылок через `pydantic`, который не модифицирует изначальную строку"""

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, value: Any) -> "HttpStr":
        if not isinstance(value, str):
            value = str(value)

        try:
            AnyHttpUrl(value)
        except Exception as e:
            raise PydanticCustomError("url_parsing", "Invalid HTTP/HTTPS URL") from e

        return cls(value)
