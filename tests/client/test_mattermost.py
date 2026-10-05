from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from pydantic import BaseModel

from src.client.mattermost import mm_client
from src.core.constants import ProjectName
from src.schemas.mattermost import MattermostTextSchema


class PayloadTestModel(BaseModel):
    notify_text: str
    channel: str


class TestMattermostClient:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("project_name", "payload_data"),
        [
            pytest.param(ProjectName.SUPP, PayloadTestModel(notify_text="ok", channel="test")),
            pytest.param(ProjectName.SUPP_DEV, PayloadTestModel(notify_text="success", channel="supp_dev_channel")),
            pytest.param(ProjectName.WB, PayloadTestModel(notify_text="alert received", channel="wildberries ch")),
        ],
    )
    async def test_post(self, mocker, project_name: ProjectName, payload_data: PayloadTestModel) -> None:
        """Имитирует отправку запроса во внешний сервис `Mattermost` и валидиует корректность ответа"""

        mock_response = MagicMock(spec=httpx.Response)
        mock_response.raise_for_status = MagicMock()

        mock_client = mocker.patch("src.client.mattermost.http_client")
        mock_client.post = AsyncMock(return_value=mock_response)

        await mm_client.post(project_name, obj_in=payload_data)

        mock_client.post.assert_called_once()
        assert mock_client.post.call_args.kwargs["obj_in"] == MattermostTextSchema(**payload_data.model_dump())
