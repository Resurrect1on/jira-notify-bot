from pydantic import computed_field

from src.core.constants import Description
from src.schemas.base_mixin import TicketAssignerBaseSchema, TicketTopicAuthorBaseSchema
from src.utils import make_hyperlink


class ExploitationCreatedTaskSchema(TicketAssignerBaseSchema, TicketTopicAuthorBaseSchema):
    """Схема для хранения данных о новой созданной задаче"""

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            "**Проект EX**:\n\n"
            f"Создано новое обращение {make_hyperlink(self.issue)}.\n"
            f"**Тема обращения**: ```{self.topic}```\n"
            f"**Автор обращения**: ```{self.author}```\n"
            f"@{self.assigner}"
        )


class ExploitationCommentSchema(TicketAssignerBaseSchema, TicketTopicAuthorBaseSchema):
    """Схема для хранения данных о новом комментарии в задаче"""

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            "**Проект EX**:\n\n"
            f"В обращении {make_hyperlink(self.issue)} был добавлен новый комментарий.\n"
            f"**Тема обращения**: ```{self.topic}```\n"
            f"**Автор комментария**: ```{self.author}```\n"
            f"@{self.assigner}"
        )
