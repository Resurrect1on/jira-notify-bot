from fastapi import APIRouter, status
from structlog import get_logger

from src.client.mattermost import mm_client
from src.core.constants import ActionType, HTTPErrorDetail, ProjectName
from src.core.route_class import ContextVarsRouterHandler
from src.schemas import (
    WildberriesAssignerSchema,
    WildberriesCommentSchema,
    WildberriesCreatedTaskSchema,
    WildberriesReOpenSchema,
)
from src.utils.make_response import make_response

router = APIRouter(route_class=ContextVarsRouterHandler)
logger = get_logger()


@router.post(
    f"/{ActionType.TASK_CREATED}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_new_created_task(obj_in: WildberriesCreatedTaskSchema) -> WildberriesCreatedTaskSchema:
    """Эндпоинт для уведомлений о создании новой задачи в проекте `WB`"""

    await mm_client.post(project_name=ProjectName.WB, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.WB, action=ActionType.TASK_CREATED)
    return obj_in


@router.post(
    f"/{ActionType.NEW_ASSIGNER}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_new_assigner(obj_in: WildberriesAssignerSchema) -> WildberriesAssignerSchema:
    """Эндпоинт для уведомлений о назначении нового исполнителя в задачах проекта `WB`"""

    await mm_client.post(project_name=ProjectName.WB, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.WB, action=ActionType.NEW_ASSIGNER)
    return obj_in


@router.post(
    f"/{ActionType.NEW_COMMENT}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_new_comment(obj_in: WildberriesCommentSchema) -> WildberriesCommentSchema:
    """Эндпоинт для уведомлений о новом комментарии в задачах проекта `WB`"""

    await mm_client.post(project_name=ProjectName.WB, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.WB, action=ActionType.NEW_COMMENT)
    return obj_in


@router.post(
    f"/{ActionType.TASK_REOPENED}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_reopened_task(obj_in: WildberriesReOpenSchema) -> WildberriesReOpenSchema:
    """Эндпоинт для уведомлений о пересоздании задач проекта `WB`"""

    await mm_client.post(project_name=ProjectName.WB, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.WB, action=ActionType.TASK_REOPENED)
    return obj_in
