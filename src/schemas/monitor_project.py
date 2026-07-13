from typing import Annotated

from pydantic import BaseModel, Field, computed_field

from src.core.constants import Description
from src.schemas.base_mixin import TicketAssignerBaseSchema
from src.service.monitor_text_builder import monitoring_service
from src.utils import make_hyperlink


class MonitoringUnfinishedTicketsSchema(BaseModel):
    """Класс для хранения данных об утреннем warning-e с количеством тикетов"""

    issues_number: Annotated[int, Field(description=Description.ISSUES_AMOUNT)]

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return monitoring_service.build(self.issues_number)


class MonitoringOutdatedTicketSchema(TicketAssignerBaseSchema):
    """Класс для хранения данных об warning-e, который просит проверить задачу, которая не обновлялась 3 дня"""

    days_without_update: Annotated[int, Field(description=Description.DAYS_WITHOUT_TASK_UPDATES)]

    @computed_field(description=Description.NOTIFY_TEXT)
    @property
    def notify_text(self) -> str:
        return (
            f"Обращение {make_hyperlink(self.issue)} необходимо обновить или закрыть, "
            "т.к. оно находится в статусе **На проверке** более трёх рабочих дней.\n"
            f"Количество дней без обновлений: **{abs(self.days_without_update)}**\n"
            f"@{self.assigner}"
        )
