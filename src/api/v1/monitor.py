from fastapi import APIRouter, HTTPException, status
from structlog import get_logger

from src.client.mattermost import mm_client
from src.core.constants import HTTPErrorDetail, ProjectName, WarningActionType
from src.core.route_class import ContextVarsRouterHandler
from src.schemas import MonitoringOutdatedTicketSchema, MonitoringUnfinishedTicketsSchema
from src.service.monitor_text_builder import monitoring_service
from src.utils.make_response import make_response

router = APIRouter(route_class=ContextVarsRouterHandler)
logger = get_logger()


@router.post(
    f"/{WarningActionType.UNFINISHED_TICKETS}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_unfinished_tickets_monitoring(
    obj_in: MonitoringUnfinishedTicketsSchema,
) -> MonitoringUnfinishedTicketsSchema:
    """Эндпоинт для уведомлений о просьбе обратить внимание на задачи в фильтре `WARNING`"""

    await mm_client.post(project_name=ProjectName.MONITOR, obj_in=obj_in)

    logger.info(
        "Сообщение в MM успешно отправлено",
        project_name=ProjectName.MONITOR,
        action=WarningActionType.UNFINISHED_TICKETS,
    )
    return obj_in


@router.post(
    f"/{WarningActionType.OUTDATED_TICKETS}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_outdated_tickets_monitoring(
    obj_in: MonitoringOutdatedTicketSchema,
) -> MonitoringOutdatedTicketSchema:
    """Эндпоинт для уведомлений о просьбе проверить задачу, которая не обновлялась 3 дня. Не посылается в выходные"""

    if not monitoring_service.is_sending_today(obj_in.days_without_update):
        logger.info(
            "Сообщение в ММ не отправлено, т.к. сегодня выходной",
            project_name=ProjectName.MONITOR,
            action=WarningActionType.OUTDATED_TICKETS,
        )
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=HTTPErrorDetail.NOT_IN_WEEKEND)

    await mm_client.post(project_name=ProjectName.MONITOR, obj_in=obj_in)

    logger.info(
        "Сообщение в MM успешно отправлено", project_name=ProjectName.MONITOR, action=WarningActionType.OUTDATED_TICKETS
    )
    return obj_in
