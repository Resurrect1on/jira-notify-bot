from typing import Any

from pydantic import BaseModel

from src.core.exceptions.schemas import ErrorMessageSchema


def make_response(
    status_code: int,
    description: str,
    model: type[BaseModel] = ErrorMessageSchema,
    *,
    example: dict[str, Any] | BaseModel | None = None,
) -> dict[int, Any]:
    """Формирует описание ответа для OpenAPI со схемой и примером"""

    example = example.model_dump() if isinstance(example, BaseModel) else example or {"detail": description}

    return {
        status_code: {"model": model, "description": description, "content": {"application/json": {"example": example}}}
    }
