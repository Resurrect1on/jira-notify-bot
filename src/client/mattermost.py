import httpx
from pydantic import BaseModel
from structlog import get_logger

from src.client import http_client
from src.core.config import settings
from src.core.constants import ProjectName
from src.core.exceptions import MattermostTransportError
from src.schemas.mattermost import MattermostTextSchema
from src.utils.custom_types import HttpStr

logger = get_logger()


class MattermostClient:
    """Клиент для интеграции с сервисом `Mattermost`"""

    _PROJECT_URL_MAPPING = {
        ProjectName.SUPP: settings.support_url,
        ProjectName.SUPP_DEV: settings.support_dev_url,
        ProjectName.SUZI: settings.suzi_url,
        ProjectName.MONITOR: settings.monitoring_url,
        ProjectName.EX: settings.ex_url,
        ProjectName.WB: settings.wb_url,
        ProjectName.CLIENT_VOICE: settings.client_voice_url,
    }

    async def post(self, project_name: ProjectName, obj_in: BaseModel, **kwargs) -> httpx.Response:
        """Метод отправляет запрос в сервис `Mattermost`"""

        url = self._get_project_url(project_name)

        try:
            response = await http_client.post(url=url, obj_in=MattermostTextSchema(**obj_in.model_dump()), **kwargs)
            response.raise_for_status()
        except Exception as error:
            logger.error(
                "Возникла ошибка при попытке отправить запрос в Mattermost",
                url=url,
                data=obj_in.model_dump(mode="json"),
            )
            raise MattermostTransportError() from error
        else:
            return response

    def _get_project_url(self, project_name: ProjectName) -> HttpStr:
        """Метод определяет корректную ссылку до проекта"""

        project_url = self._PROJECT_URL_MAPPING.get(project_name)
        if not project_url:
            raise KeyError("Неизвестное наименование проекта")

        return project_url


mm_client = MattermostClient()
