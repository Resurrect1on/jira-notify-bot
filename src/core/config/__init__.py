from typing import Annotated

from pydantic import Field, computed_field
from pydantic_settings import SettingsConfigDict

from src.schemas.base_mixin import BaseSettingsMixin
from src.utils.custom_types import HttpStr


class BaseSettingsConfig(BaseSettingsMixin):
    model_config = SettingsConfigDict(extra="allow", case_sensitive=False)


class Settings(BaseSettingsConfig):
    version: Annotated[str, Field(description="Версия приложения")]
    mattermost_url: Annotated[HttpStr, Field(description="Виртуальный основной адрес маттермоста")]
    timeout_seconds: Annotated[int, Field(60, description="Стандартный интервал в секундах для таймаута")]
    debug: Annotated[bool, Field(False, description="Уровень логгирования")]
    default_backoff_max_tries: Annotated[
        int, Field(3, description="Максимальное количество попыток для ретрая в декораторе backoff")
    ]

    support_project_hook: Annotated[str, Field(description="Уникальный идентификатор интеграции с чатом SUPPORT")]
    support_dev_project_hook: Annotated[str, Field(description="Уникальный идентификатор интеграции с чатом SUPP-DEV")]
    suzi_project_hook: Annotated[str, Field(description="Уникальный идентификатор интеграции с чатом SUZI")]
    ex_project_hook: Annotated[str, Field(description="Уникальный идентификатор интеграции с чатом EXPLOITATION")]
    wb_project_hook: Annotated[str, Field(description="Уникальный идентификатор интеграции с чатом WILDBERRIES")]
    monitoring_hook: Annotated[str, Field(description="Уникальный идентификатор интеграции с чатом MONITORING")]
    client_voice_hook: Annotated[str, Field(description="Уникальный идентификатор интеграции с чатом CLIENT-VOICE")]

    @computed_field(description="Ссылка до интеграции с проектом SUPPORT")
    @property
    def support_url(self) -> HttpStr:
        return HttpStr(f"{self.mattermost_url}/{self.support_project_hook}")

    @computed_field(description="Ссылка до интеграции с проектом SUPP-DEV")
    @property
    def support_dev_url(self) -> HttpStr:
        return HttpStr(f"{self.mattermost_url}/{self.support_dev_project_hook}")

    @computed_field(description="Ссылка до интеграции с проектом SUZI")
    @property
    def suzi_url(self) -> HttpStr:
        return HttpStr(f"{self.mattermost_url}/{self.suzi_project_hook}")

    @computed_field(description="Ссылка до интеграции с проектом EXPLOITATION")
    @property
    def ex_url(self) -> HttpStr:
        return HttpStr(f"{self.mattermost_url}/{self.ex_project_hook}")

    @computed_field(description="Ссылка до интеграции с проектом WILDBERRIES")
    @property
    def wb_url(self) -> HttpStr:
        return HttpStr(f"{self.mattermost_url}/{self.wb_project_hook}")

    @computed_field(description="Ссылка до интеграции с проектом MONITORING")
    @property
    def monitoring_url(self) -> HttpStr:
        return HttpStr(f"{self.mattermost_url}/{self.monitoring_hook}")

    @computed_field(description="Ссылка до интеграции с проектом CLIENT-VOICE")
    @property
    def client_voice_url(self) -> HttpStr:
        return HttpStr(f"{self.mattermost_url}/{self.client_voice_hook}")


settings = Settings()  # type: ignore
