from fastapi import APIRouter, Depends

from backend.core.fastapi.dependencies.authentication import AuthenticationRequired

from .sessions import session_router

sessions_router = APIRouter()
sessions_router.include_router(
    session_router,
    tags=["Sessions"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["sessions_router"]
