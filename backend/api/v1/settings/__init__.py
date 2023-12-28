from fastapi import APIRouter, Depends

from backend.core.fastapi.dependencies.authentication import AuthenticationRequired

from .aimodels import ai_model_router

settings_router = APIRouter()
settings_router.include_router(
    ai_model_router,
    tags=["Settings"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["settings_router"]
