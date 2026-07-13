from fastapi import APIRouter, status
from structlog import get_logger

from src.client.mattermost import mm_client
from src.core.constants import CSAT_SCORE_TO_SEND_NOTIFY, ActionType, HTTPErrorDetail, ProjectName
from src.core.route_class import ContextVarsRouterHandler
from src.schemas import ClientVoiceCreatedTaskSchema, ClientVoiceModifiedTaskSchema, ClientVoiceSatisfactionSchema
from src.utils.make_response import make_response

router = APIRouter(route_class=ContextVarsRouterHandler)
logger = get_logger()


@router.post(
    f"/{ActionType.TASK_CREATED}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_new_created_task(obj_in: ClientVoiceCreatedTaskSchema) -> ClientVoiceCreatedTaskSchema:
    """Эндпоинт для уведомлений о создании новой задачи в проекте `SZO` - `Client voice`"""

    await mm_client.post(project_name=ProjectName.CLIENT_VOICE, obj_in=obj_in)

    logger.info(
        "Сообщение в MM успешно отправлено", project_name=ProjectName.CLIENT_VOICE, action=ActionType.TASK_CREATED
    )
    return obj_in


@router.post(
    f"/{ActionType.TASK_MODIFIED}",
    status_code=status.HTTP_200_OK,
    responses={**make_response(status.HTTP_503_SERVICE_UNAVAILABLE, HTTPErrorDetail.MATTERMOST_UNAVAILABLE)},
)
async def listen_to_task_updates(obj_in: ClientVoiceModifiedTaskSchema) -> ClientVoiceModifiedTaskSchema:
    """Эндпоинт для уведомлений об обновлении существующей задачи в проекте `SZO` - `Client voice`"""

    await mm_client.post(project_name=ProjectName.CLIENT_VOICE, obj_in=obj_in)

    logger.info(
        "Сообщение в MM успешно отправлено", project_name=ProjectName.CLIENT_VOICE, action=ActionType.TASK_MODIFIED
    )
    return obj_in


@router.post(f"/{ActionType.ADDED_CSAT_SATISFACTION}", status_code=status.HTTP_200_OK, responses={})
async def listen_to_user_reviews(obj_in: ClientVoiceSatisfactionSchema) -> ClientVoiceSatisfactionSchema:
    """Эндпоинт для уведомлений об удовлетворённости пользователей в проекте `SZO` - `Client voice`"""

    if obj_in.score <= CSAT_SCORE_TO_SEND_NOTIFY:
        await mm_client.post(project_name=ProjectName.CLIENT_VOICE, obj_in=obj_in)
        logger.info(
            "Сообщение в MM успешно отправлено",
            project_name=ProjectName.CLIENT_VOICE,
            action=ActionType.ADDED_CSAT_SATISFACTION,
        )

    return obj_in
