from fastapi import APIRouter, status
from structlog import get_logger

from src.client.mattermost import mm_client
from src.core.constants import ActionType, HTTPErrorDetail, ProjectName
from src.core.route_class import ContextVarsRouterHandler
from src.schemas import SuziCommentSchema, SuziDevUpdateTaskSchema
from src.utils.make_response import make_response

router = APIRouter(route_class=ContextVarsRouterHandler)
logger = get_logger()


@router.post(
    f"/{ActionType.NEW_COMMENT}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_new_comment(obj_in: SuziCommentSchema) -> SuziCommentSchema:
    """Эндпоинт для уведомлений о новом комментарии в задачах проекта `SUZI`"""

    await mm_client.post(project_name=ProjectName.SUZI, obj_in=obj_in)

    logger.info("Сообщение в MM успешно отправлено", project_name=ProjectName.SUZI, action=ActionType.NEW_COMMENT)
    return obj_in


@router.post(
    f"/dev/{ActionType.TASK_CREATED}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_dev_modified_component(obj_in: SuziDevUpdateTaskSchema) -> SuziDevUpdateTaskSchema:
    """Эндпоинт для уведомлений о создании `SUZI` задачи в `Dev-Supp` проекте"""

    await mm_client.post(project_name=ProjectName.SUPP_DEV, obj_in=obj_in)

    logger.info("Сообщение в ММ успешно отправлено", project_name=ProjectName.SUPP_DEV, action=ActionType.TASK_CREATED)
    return obj_in
