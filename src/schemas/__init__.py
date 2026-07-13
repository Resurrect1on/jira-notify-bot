from src.schemas.client_voice import (
    ClientVoiceCreatedTaskSchema,
    ClientVoiceModifiedTaskSchema,
    ClientVoiceSatisfactionSchema,
)
from src.schemas.ex_project import ExploitationCommentSchema, ExploitationCreatedTaskSchema
from src.schemas.monitor_project import MonitoringOutdatedTicketSchema, MonitoringUnfinishedTicketsSchema
from src.schemas.support_project import (
    SupportAssignerSchema,
    SupportCommentSchema,
    SupportCreatedTaskSchema,
    SupportReOpenSchema,
)
from src.schemas.suzi_project import SuziCommentSchema, SuziDevUpdateTaskSchema
from src.schemas.wb_project import (
    WildberriesAssignerSchema,
    WildberriesCommentSchema,
    WildberriesCreatedTaskSchema,
    WildberriesReOpenSchema,
)

__all__ = [
    "ClientVoiceCreatedTaskSchema",
    "ClientVoiceModifiedTaskSchema",
    "ClientVoiceSatisfactionSchema",
    "ExploitationCommentSchema",
    "ExploitationCreatedTaskSchema",
    "MonitoringOutdatedTicketSchema",
    "MonitoringUnfinishedTicketsSchema",
    "SupportAssignerSchema",
    "SupportCommentSchema",
    "SupportCreatedTaskSchema",
    "SupportReOpenSchema",
    "SuziCommentSchema",
    "SuziDevUpdateTaskSchema",
    "WildberriesAssignerSchema",
    "WildberriesCommentSchema",
    "WildberriesCreatedTaskSchema",
    "WildberriesReOpenSchema",
]
