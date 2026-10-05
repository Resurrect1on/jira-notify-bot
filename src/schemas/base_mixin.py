from typing import Annotated, Any

from pydantic import BaseModel, Field, SecretStr, computed_field, field_serializer
from pydantic_settings import BaseSettings

from src.core.constants import Description
from src.utils import make_hyperlink


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


class TicketSatisfactionBaseSchema(TicketBaseSchema):
    """
    Базовый продвинутый класс для хранения информации об оценке и комментарии пользователя.
    Поля для наследования: `issue`, `score`, `comment`
    """

    score: Annotated[int, Field(description=Description.CSAT_SCORE)]
    comment: Annotated[str | None, Field(description=Description.CSAT_COMMENT)] = None

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            f"Уведомление о низкой оценке удовлетворенности: {make_hyperlink(self.issue)}.\n\n"
            f"**Оценка пользователя**: ```{self.score}```\n"
            # f"**Комментарий пользователя**: ```{self.comment or '-'}```"
        )


class BaseSettingsMixin(BaseSettings):
    """Класс для правильной сериализации всех полей с типом `SecretStr`"""

    @field_serializer("*", when_used="always")
    def serialize_secret_fields(self, value: Any) -> Any:
        if isinstance(value, SecretStr):
            return value.get_secret_value()

        return value
