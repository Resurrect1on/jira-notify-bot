import datetime
from typing import Annotated

from pydantic import Field, computed_field

from src.core.constants import Description
from src.schemas.base_mixin import TicketAssignerBaseSchema, TicketTopicAuthorBaseSchema
from src.utils import make_hyperlink


class SuziCommentSchema(TicketAssignerBaseSchema, TicketTopicAuthorBaseSchema):
    """Схема для хранения данных о новом комментарии в задаче"""

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            "**Проект SUZI**:\n\n"
            f"В обращении {make_hyperlink(self.issue)} был добавлен новый комментарий.\n"
            f"**Тема обращения**: ```{self.topic}```\n"
            f"**Автор комментария**: ```{self.author}```\n"
            f"@{self.assigner}"
        )


class SuziDevUpdateTaskSchema(TicketTopicAuthorBaseSchema):
    """Схема для хранения данных о созданной `SUZI` задаче для проекта `Dev-ТП`"""

    system_object: Annotated[str | None, Field(description=Description.SYSTEM_OBJECT)]
    components: Annotated[str | None, Field(description=Description.TASK_COMPONENTS)]
    marks: Annotated[str | None, Field(description=Description.TASK_MARKS)]
    clients: Annotated[str | None, Field(description=Description.CLIENTS)]
    created_at: Annotated[datetime.date, Field(description=Description.TASK_CREATED_DATE)]

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            f"Создано новое обращение {make_hyperlink(self.issue)}.\n\n"
            f"**Тема обращения**: ```{self.topic}```\n"
            f"**Автор обращения**: ```{self.author}```\n"
            f"**Объект системы**: ```{self.system_object or 'Не указан'}```\n"
            f"**Компоненты**: ```{self.components or 'Не заполнено'}```\n"
            f"**Метки**: ```{self.marks or 'Не заполнено'}```\n"
            f"**Организации**: ```{self.clients or 'Не указаны'}```\n"
            f"**Дата создания обращения**: ```{self.created_at}```\n"
            f"**Срок реакции**: ```48 часов```"
        )
