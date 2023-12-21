from fastapi import APIRouter, Depends

from backend.core.fastapi.dependencies.authentication import AuthenticationRequired

from .chatbots import chatbot_router

chatbots_router = APIRouter()
chatbots_router.include_router(
    chatbot_router,
    tags=["Chatbots"],
    dependencies=[Depends(AuthenticationRequired)],
)

__all__ = ["chatbots_router"]
