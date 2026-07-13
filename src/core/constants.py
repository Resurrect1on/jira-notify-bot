from enum import IntEnum, StrEnum

# Максимальная оценка пользователя для уведомления в канал
CSAT_SCORE_TO_SEND_NOTIFY = 2
# Количество дней для отправки сообщения о необходимости обновить/закрыть задачу
DAYS_WITHOUT_UPDATE_TRIGGER = 5


class Weekday(IntEnum):
    """Дни недели"""

    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class HTTPErrorDetail(StrEnum):
    """Описание `HTTP`-ошибок"""

    INTERNAL_ERROR_RESPONSE = "Internal error response"
    MATTERMOST_UNAVAILABLE = "Mattermost service is unavailable at the moment. Try again later.."
    NOT_IN_WEEKEND = "We got your request successfully, but we won't proceed it because of the current weekday"
    SERVICE_UNAVAILABLE = "Integration service is unavailable"
    UNKNOWN_ERROR_RESPONSE = "Unknown error"
    UNPROCESSABLE_ENTITY_ERROR_RESPONSE = "Unprocessable entity error"


class ProjectName(StrEnum):
    """Наименование проекта в `Jira`"""

    CLIENT_VOICE = "client_voice"
    EX = "exploitation"
    MONITOR = "monitoring"
    SUPP = "support"
    SUPP_DEV = "support-dev"
    SUZI = "suzi"
    WB = "wildberries"


class ActionType(StrEnum):
    """Наименование действия в `Jira`"""

    ADDED_CSAT_SATISFACTION = "satisfaction"
    NEW_ASSIGNER = "assigner"
    NEW_COMMENT = "comment"
    TASK_CREATED = "created"
    TASK_MODIFIED = "modified"
    TASK_REOPENED = "reopened"


class WarningActionType(StrEnum):
    """Наименование действий для `Warning`-ов"""

    OUTDATED_TICKETS = "outdated"
    UNFINISHED_TICKETS = "unfinished"


class Description(StrEnum):
    """Текстовые описания различных аттрибутов"""

    ASSIGNER_NAME = "Имя исполнителя задачи"
    AUTHOR_NAME = "Имя автора"
    CLIENTS = "Список клиентов (организаций) через запятую"
    CSAT_COMMENT = "Текстовая оценка пользователя"
    CSAT_SCORE = "Оценка пользователя"
    DAYS_WITHOUT_TASK_UPDATES = "Количество дней, которые не обновлялась задача"
    ERRORS_LIST = "Массив с ошибками"
    ERROR_DETAILS = "Подробное описание деталей ошибки"
    ERROR_MESSAGE = "Описание ошибки"
    FIELD = "Поле с ошибкой"
    ISSUES_AMOUNT = "Количество обращений"
    ISSUE_NUMBER = "Номер задачи"
    IS_MAJOR_CLIENT = "Флаг крупного клиента"
    NOTIFY_TEXT = "Текст уведомления"
    SUBJECT_ITN = "ИНН субъекта"
    SYSTEM_OBJECT = "Объект системы"
    TASK_COMPONENTS = "Компоненты задачи"
    TASK_CREATED_DATE = "Дата создания задачи"
    TASK_DESCRIPTION = "Описание задачи"
    TASK_MARKS = "Метки задачи"
    TASK_TOPIC = "Тема задачи"
