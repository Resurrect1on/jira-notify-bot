from typing import Annotated

from pydantic import BaseModel, Field

from src.core.constants import Description


class MattermostTextSchema(BaseModel):
    """Класс для отправки `HTTP` запросов во внешний интеграционный сервис `Mattermost`"""

    text: Annotated[str, Field(alias="notify_text", description=Description.NOTIFY_TEXT)]
