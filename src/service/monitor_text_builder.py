import datetime

from structlog import get_logger

from src.core.constants import DAYS_WITHOUT_UPDATE_TRIGGER, Weekday

logger = get_logger()


class MonitoringTextBuilder:
    """Класс для формирования текстовки сообщений по мониторингу"""

    _WEEKDAY_MAPPING = {
        Weekday.MONDAY: "Понедельник",
        Weekday.TUESDAY: "Вторник",
        Weekday.WEDNESDAY: "Среда",
        Weekday.THURSDAY: "Четверг",
        Weekday.FRIDAY: "Пятница",
        Weekday.SATURDAY: "Суббота",
        Weekday.SUNDAY: "Воскресенье",
    }

    _AUTOMATIC_MESSAGE_TEMPLATE = (
        ":fire: Утреннее автоматическое сообщение. :fire:\n\n"
        "{cyrillic_weekday}, {current_day}.\n"
        "В данный момент у нас **{issues_number}** {correct_ending} в фильтре **Warning**, "
        "просьба обратить на них внимание"
    )

    def build(self, issues_number: int) -> str:
        cyrillic_weekday = self._get_cyrillic_weekday()
        current_day = datetime.date.today().isoformat()
        last_int_digit = self._get_last_issue_digit(issues_number)
        last_two_digits = issues_number % 100

        if 11 <= last_two_digits <= 14:  # noqa: PLR2004
            correct_ending = "обращений"
        elif last_int_digit == 1:
            correct_ending = "обращение"
        elif last_int_digit in (2, 3, 4):
            correct_ending = "обращения"
        else:
            correct_ending = "обращений"

        return self._AUTOMATIC_MESSAGE_TEMPLATE.format(
            cyrillic_weekday=cyrillic_weekday,
            current_day=current_day,
            issues_number=issues_number,
            correct_ending=correct_ending,
        )

    @staticmethod
    def is_sending_today(days_without_update: int) -> bool:
        """
        Метод определяет будет ли отправлено уведомление о незакрытой задаче.

        #### Уведомление отправляется при следующих условиях:
            - Сегодняшний день не должен быть выходным (Воскресенье или Суббота)
            - Сегодняшний день является Средой, Четвергом или Пятницей
            - Сегодняшний день является Понедельником или Вторником.
                И задача должна была не обновляться более 5 дней подряд
        """

        weekday = datetime.datetime.today().weekday()
        return bool(
            weekday in range(2, 5)
            or (weekday < Weekday.WEDNESDAY and days_without_update > DAYS_WITHOUT_UPDATE_TRIGGER)
        )

    def _get_last_issue_digit(self, issues_number: int) -> int:
        last_str_digit = str(issues_number)[-1]
        return int(last_str_digit)

    def _get_cyrillic_weekday(self) -> str:
        number = datetime.datetime.today().weekday()
        return self._WEEKDAY_MAPPING[number]  # pyright: ignore[reportArgumentType]


monitoring_service = MonitoringTextBuilder()
