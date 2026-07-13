from fastapi import APIRouter

from src.api.v1 import client_voice, exploitation, monitor, support, suzi, wildberries

app_router = APIRouter(prefix="/v1")

app_router.include_router(client_voice.router, prefix="/client-voice", tags=["client voice"])
app_router.include_router(exploitation.router, prefix="/exploitation", tags=["exploitation"])
app_router.include_router(monitor.router, prefix="/monitor", tags=["monitor"])
app_router.include_router(support.router, prefix="/support", tags=["support"])
app_router.include_router(suzi.router, prefix="/suzi", tags=["suzi"])
app_router.include_router(wildberries.router, prefix="/wb", tags=["wb"])
