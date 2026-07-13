from typing import Annotated, Any

from pydantic import BaseModel, Field, SecretStr, field_serializer
from pydantic_settings import BaseSettings

from src.core.constants import Description


class TicketBaseSchema(BaseModel):
    """Базовый класс для наследования полей (`issue`)"""

    issue: Annotated[str, Field(description=Description.ISSUE_NUMBER)]


class TicketAssignerBaseSchema(TicketBaseSchema):
    """Базовый продвинутый класс с доп. полями для наследования (`issue`, `assigner`)"""

    assigner: Annotated[str, Field(description=Description.ASSIGNER_NAME)]


class TicketTopicAuthorBaseSchema(TicketBaseSchema):
    """Базовый продвинутый класс с доп. полями для наследования (`issue`, `topic`, `author`)"""

    topic: Annotated[str, Field(description=Description.TASK_TOPIC)]
    author: Annotated[str, Field(description=Description.AUTHOR_NAME)]


class BaseSettingsMixin(BaseSettings):
    """Класс для правильной сериализации всех полей с типом `SecretStr`"""

    @field_serializer("*", when_used="always")
    def serialize_secret_fields(self, value: Any) -> Any:
        if isinstance(value, SecretStr):
            return value.get_secret_value()

        return value
