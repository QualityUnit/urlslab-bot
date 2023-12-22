from fastapi import APIRouter, Depends

from backend.core.fastapi.dependencies.authentication import AuthenticationRequired

from .documents import document_router

documents_router = APIRouter()
documents_router.include_router(
    document_router,
    tags=["Documents"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["documents_router"]
