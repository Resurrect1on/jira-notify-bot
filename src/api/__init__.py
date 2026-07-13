from fastapi import APIRouter

from src.api import v1

app_router = APIRouter(prefix="/api")

app_router.include_router(v1.app_router)
