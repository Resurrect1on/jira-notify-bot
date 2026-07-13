import datetime
from typing import Annotated

from pydantic import Field, computed_field

from src.core.constants import Description
from src.schemas.base_mixin import TicketBaseSchema
from src.utils import make_hyperlink


class ClientVoiceBaseSchema(TicketBaseSchema):
    """
    Базовая схема для хранения информации об обращении в проекте `SZO` - `Client voice`

    Args:
        `issue` (str): Номер задачи
        `topic` (str): Тема задачи
        `description` (str): Описание задачи
        `created_at` (datetime.date): Дата создания обращения
        `is_major` (str | None): Флаг крупного клиента
        `itn` (str | None): ИНН субъекта
    """

    topic: Annotated[str, Field(description=Description.TASK_TOPIC)]
    description: Annotated[str, Field(description=Description.TASK_DESCRIPTION)]
    created_at: Annotated[datetime.date, Field(description=Description.TASK_CREATED_DATE)]
    is_major: Annotated[str | None, Field(description=Description.IS_MAJOR_CLIENT)] = None
    itn: Annotated[str | None, Field(description=Description.SUBJECT_ITN)] = None


class ClientVoiceCreatedTaskSchema(ClientVoiceBaseSchema):
    """
    Схема для хранения информации о созданном обращении в проекте `SZO` - `Client voice`

    Args:
        `issue` (str): Номер задачи
        `topic` (str): Тема задачи
        `description` (str): Описание задачи
        `created_at` (datetime.date): Дата создания обращения
        `is_major` (str | None): Флаг крупного клиента
        `itn` (str | None): ИНН субъекта
    """

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            f"Обращение создано: {make_hyperlink(self.issue)}.\n\n"
            f"**Тема обращения**: ```{self.topic}```\n"
            # f"**Описание задачи**: ```{self.description}```\n"
            f"**ИНН Субъекта**: ```{self.itn or '-'}```\n"
            f"**Крупный клиент**: ```{self.is_major or 'Нет'}```\n"
            f"**Дата создания обращения**: ```{self.created_at}```"
        )


class ClientVoiceModifiedTaskSchema(ClientVoiceBaseSchema):
    """
    Схема для хранения информации о изменённом обращении в проекте `SZO` - `Client voice`

    Args:
        `issue` (str): Номер задачи
        `topic` (str): Тема задачи
        `description` (str): Описание задачи
        `created_at` (datetime.date): Дата создания обращения
        `is_major` (str | None): Флаг крупного клиента
        `itn` (str | None): ИНН субъекта
    """

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            f"Обращение обновлено: {make_hyperlink(self.issue)}.\n\n"
            f"**Тема обращения**: ```{self.topic}```\n"
            # f"**Описание задачи**: ```{self.description}```\n"
            f"**ИНН Субъекта**: ```{self.itn or '-'}```\n"
            f"**Крупный клиент**: ```{self.is_major or 'Нет'}```\n"
            f"**Дата создания обращения**: ```{self.created_at}```"
        )


class ClientVoiceSatisfactionSchema(TicketBaseSchema):
    """
    Схема для хранения информации об оценка и комментарии пользователя в проекте `SZO` - `Client voice`

    Args:
        `issue` (str): Номер задачи
        `score` (int): Оценка пользователя
        `comment` (str): Текстовый комментарий пользователя
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
