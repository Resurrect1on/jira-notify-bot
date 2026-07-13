from pydantic import computed_field

from src.core.constants import Description
from src.schemas.base_mixin import TicketAssignerBaseSchema, TicketTopicAuthorBaseSchema
from src.utils import make_hyperlink


class WildberriesCreatedTaskSchema(TicketTopicAuthorBaseSchema):
    """Схема для хранения данных о новой созданной задаче"""

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            "@support @watchdog\n\n"
            f"Создано новое обращение {make_hyperlink(self.issue)}.\n"
            f"**Тема обращения**: ```{self.topic}```\n"
            f"**Автор обращения**: ```{self.author}```"
        )


class WildberriesAssignerSchema(TicketAssignerBaseSchema):
    """Схема для хранения данных о назначении нового исполнителя в задаче"""

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return f"В тикете {make_hyperlink(self.issue)} назначен новый исполнитель.\n@{self.assigner}"


class WildberriesCommentSchema(TicketAssignerBaseSchema):
    """Схема для хранения данных о новом комментарии в задаче"""

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return f"В тикете {make_hyperlink(self.issue)} появился новый ответ.\n@{self.assigner}\n@watchdog"


class WildberriesReOpenSchema(TicketAssignerBaseSchema, TicketTopicAuthorBaseSchema):
    """Схема для хранения данных о переоткрытии задачи"""

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            f"Закрытый тикет {make_hyperlink(self.issue)} был переоткрыт.\n"
            f"**Тема обращения**: ```{self.topic}```\n"
            f"**Автор**: ```{self.author}```\n"
            f"@{self.assigner}"
        )
