from fastapi import APIRouter, status
from structlog import get_logger

from src.client.mattermost import mm_client
from src.core.constants import CSAT_SCORE_TO_SEND_NOTIFY, ActionType, HTTPErrorDetail, ProjectName
from src.core.route_class import ContextVarsRouterHandler
from src.schemas import (
    SupportAssignerSchema,
    SupportCommentSchema,
    SupportCreatedTaskSchema,
    SupportReOpenSchema,
    SupportSatisfactionSchema,
)
from src.utils.make_response import make_response

router = APIRouter(route_class=ContextVarsRouterHandler)
logger = get_logger()


@router.post(
    f"/{ActionType.TASK_CREATED}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_new_created_task(obj_in: SupportCreatedTaskSchema) -> SupportCreatedTaskSchema:
    """Эндпоинт для уведомлений о создании новой задачи в проекте `SUPP`"""

    await mm_client.post(project_name=ProjectName.SUPP, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.SUPP, action=ActionType.TASK_CREATED)
    return obj_in


@router.post(
    f"/{ActionType.NEW_ASSIGNER}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_new_assigner(obj_in: SupportAssignerSchema) -> SupportAssignerSchema:
    """Эндпоинт для уведомлений о назначении нового исполнителя в задачах проекта `SUPP`"""

    await mm_client.post(project_name=ProjectName.SUPP, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.SUPP, action=ActionType.NEW_ASSIGNER)
    return obj_in


@router.post(
    f"/{ActionType.NEW_COMMENT}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_new_comment(obj_in: SupportCommentSchema) -> SupportCommentSchema:
    """Эндпоинт для уведомлений о новом комментарии в задачах проекта `SUPP`"""

    await mm_client.post(project_name=ProjectName.SUPP, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.SUPP, action=ActionType.NEW_COMMENT)
    return obj_in


@router.post(
    f"/{ActionType.TASK_REOPENED}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_reopened_task(obj_in: SupportReOpenSchema) -> SupportReOpenSchema:
    """Эндпоинт для уведомлений о пересоздании задач проекта `SUPP`"""

    await mm_client.post(project_name=ProjectName.SUPP, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.SUPP, action=ActionType.TASK_REOPENED)
    return obj_in


@router.post(f"/{ActionType.ADDED_CSAT_SATISFACTION}", status_code=status.HTTP_200_OK, responses={})
async def listen_to_user_reviews(obj_in: SupportSatisfactionSchema) -> SupportSatisfactionSchema:
    """Эндпоинт для уведомлений об удовлетворённости пользователей в проекте `SUPP` - `CSAT`"""

    if obj_in.score <= CSAT_SCORE_TO_SEND_NOTIFY:
        await mm_client.post(project_name=ProjectName.SUPP_CSAT, obj_in=obj_in)
        logger.info(
            "Сообщение в MM успешно отправлено",
            project_name=ProjectName.SUPP_CSAT,
            action=ActionType.ADDED_CSAT_SATISFACTION,
        )

    return obj_in
