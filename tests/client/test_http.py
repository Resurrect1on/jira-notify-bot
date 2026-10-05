from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from pydantic import BaseModel

from src.client.http import HttpClient
from src.core.constants import RequestMethodName

TEST_API_URL = "https://api.test/v1/request"


class PayloadTestModel(BaseModel):
    name: str
    count: int


@pytest.fixture
def client() -> HttpClient:
    return HttpClient()


class TestHttpClient:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("method_name", "payload_data", "expected_json"),
        [
            pytest.param(RequestMethodName.GET, None, None, id="get_empty_body"),
            pytest.param(RequestMethodName.PATCH, None, None, id="patch_empty_body"),
            pytest.param(
                RequestMethodName.POST,
                PayloadTestModel(name="some_data", count=5),
                {"name": "some_data", "count": 5},
                id="post_with_body",
            ),
        ],
    )
    async def test_request_method(
        self,
        mocker,
        client: HttpClient,
        method_name: RequestMethodName,
        payload_data: PayloadTestModel | None,
        expected_json: dict | None,
    ) -> None:
        """Имитирует отправку запроса к внешнему источнику и валидирует корректность ответа"""

        mock_response = MagicMock(spec=httpx.Response)
        mock_response.raise_for_status = MagicMock()

        mock_context_manager = mocker.patch("src.client.http.async_http_client")
        mock_client = mock_context_manager.return_value.__aenter__.return_value
        mock_client.request = AsyncMock(return_value=mock_response)

        await client._request(method_name, url=TEST_API_URL, obj_in=payload_data)

        mock_client.request.assert_called_once()
        assert mock_client.request.call_args.kwargs["json"] == expected_json
        assert str(mock_client.request.call_args.kwargs["url"]) == TEST_API_URL
