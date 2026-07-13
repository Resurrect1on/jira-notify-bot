import datetime
from collections.abc import Generator

import pytest

from src.service.monitor_text_builder import MonitoringTextBuilder


def mock_datetime(year: int, month: int, day: int) -> type[datetime.datetime]:
    class MockDateTime(datetime.datetime):
        @classmethod
        def today(cls):
            return cls(year, month, day)

    return MockDateTime


@pytest.fixture
def monitoring_text_builder():
    return MonitoringTextBuilder()


class TestMonitoringTextBuilder:
    @pytest.fixture(autouse=True)
    def _setup(self, monitoring_text_builder: MonitoringTextBuilder) -> Generator[None]:
        self.builder = monitoring_text_builder

        yield


@pytest.mark.parametrize(
    ("issues", "ending"),
    [
        pytest.param(0, "обращений", id="zero"),
        pytest.param(1, "обращение", id="one"),
        pytest.param(2, "обращения", id="two"),
        pytest.param(3, "обращения", id="three"),
        pytest.param(4, "обращения", id="four"),
        pytest.param(5, "обращений", id="five"),
        pytest.param(8, "обращений", id="eight"),
        pytest.param(9, "обращений", id="nine"),
        pytest.param(10, "обращений", id="ten"),
        pytest.param(11, "обращений", id="eleven"),
        pytest.param(12, "обращений", id="twelve"),
        pytest.param(13, "обращений", id="thirteen"),
        pytest.param(14, "обращений", id="fourteen"),
        pytest.param(15, "обращений", id="fifteen"),
        pytest.param(20, "обращений", id="twenty"),
        pytest.param(21, "обращение", id="twenty-one"),
        pytest.param(22, "обращения", id="twenty-two"),
        pytest.param(23, "обращения", id="twenty-three"),
        pytest.param(24, "обращения", id="twenty-four"),
        pytest.param(25, "обращений", id="twenty-five"),
        pytest.param(51, "обращение", id="fifty-one"),
        pytest.param(62, "обращения", id="sixty-two"),
        pytest.param(111, "обращений", id="one-hundred-eleven"),
        pytest.param(112, "обращений", id="one-hundred-twelve"),
        pytest.param(113, "обращений", id="one-hundred-thirteen"),
        pytest.param(114, "обращений", id="one-hundred-fourteen"),
        pytest.param(213, "обращений", id="two-hundred-thirteen"),
    ],
)
def test_build_correct_word_ending(issues: int, ending: str) -> None:
    """Выполняет проверку корректного окончания сообщения в зависимости от количества обращений"""

    text = MonitoringTextBuilder().build(issues)

    assert f"**{issues}** {ending}" in text


@pytest.mark.parametrize(
    ("datetime_mock", "days_without_update", "result"),
    [
        # Понедельник
        pytest.param(mock_datetime(2026, 7, 6), 5, False, id="monday-threshold"),
        pytest.param(mock_datetime(2026, 7, 6), 6, True, id="monday-above-threshold"),
        # Вторник
        pytest.param(mock_datetime(2026, 7, 7), 5, False, id="tuesday-threshold"),
        pytest.param(mock_datetime(2026, 7, 7), 6, True, id="tuesday-above-threshold"),
        # Среда
        pytest.param(mock_datetime(2026, 7, 8), 0, True, id="wednesday-no-delay"),
        pytest.param(mock_datetime(2026, 7, 8), 100, True, id="wednesday-long-delay"),
        # Четверг
        pytest.param(mock_datetime(2026, 7, 9), 0, True, id="thursday-no-delay"),
        # Пятница
        pytest.param(mock_datetime(2026, 7, 10), 0, True, id="friday-no-delay"),
        # Выходные
        pytest.param(mock_datetime(2026, 7, 11), 0, False, id="saturday"),
        pytest.param(mock_datetime(2026, 7, 11), 100, False, id="saturday-long-delay"),
        pytest.param(mock_datetime(2026, 7, 12), 0, False, id="sunday"),
        pytest.param(mock_datetime(2026, 7, 12), 100, False, id="sunday-long-delay"),
    ],
)
def test_is_sending_today_on_wednesday(
    monkeypatch, datetime_mock: datetime.datetime, days_without_update: int, result: bool
) -> None:
    """Проверяет решение об отправке уведомления для разных дней недели и количества дней без обновления"""

    monkeypatch.setattr(datetime, "datetime", datetime_mock)

    assert MonitoringTextBuilder.is_sending_today(days_without_update) is result
