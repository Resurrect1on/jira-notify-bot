import pytest
from pydantic_core import PydanticCustomError

from src.utils.custom_types import HttpStr


@pytest.mark.parametrize(
    ("url"),
    [
        pytest.param("http://url.com"),
        pytest.param("https://randomurl.hub.io"),
        pytest.param("https://пример.рф/путь"),
        pytest.param("https://пример.москва/путь"),
        pytest.param("http://example.com"),
        pytest.param("https://example.com/section1"),
    ],
)
def test_correct_http_custom_class_validation(url: str) -> None:
    """Выполняет валидацию корректной ссылки"""

    HttpStr.validate(url)


@pytest.mark.parametrize(
    ("url"),
    [
        pytest.param(""),
        pytest.param(" "),
        pytest.param("http://"),
        pytest.param("https://"),
        pytest.param("http//test.ru"),
        pytest.param("https://#=&?.com"),
        pytest.param("https://example:.com"),
        pytest.param("htp://example.com"),
        pytest.param("www.example.com"),
    ],
)
def test_incorrect_http_custom_class_validation(url: str) -> None:
    """Выполняет валидацию некорректной ссылки"""

    with pytest.raises(PydanticCustomError):
        HttpStr.validate(url)
