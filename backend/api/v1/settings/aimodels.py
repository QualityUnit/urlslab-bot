from fastapi import APIRouter, Depends, Request, Security

from app.controllers.aimodels import SettingsController
from app.schemas.responses.aimodel import EmbeddingModelResponse
from core.factory import Factory

ai_model_router = APIRouter()


@ai_model_router.get("/embedding-model", response_model=EmbeddingModelResponse)
def get_embedding_model(
        ai_model_controller: SettingsController = Depends(Factory().get_ai_model_controller),
) -> EmbeddingModelResponse:
    return ai_model_controller.get_embedding_model()
