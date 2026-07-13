from src.utils.formatted_str import hyperlink, jira_link


def make_hyperlink(issue_name: str) -> str:
    """Функция возвращает строку для гиперссылки"""

    return hyperlink.format(text=issue_name, url=jira_link.format(issue=issue_name))
