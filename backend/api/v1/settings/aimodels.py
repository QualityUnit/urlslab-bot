from fastapi import APIRouter, Depends, Request, Security

from backend.app.controllers.aimodels import SettingsController
from backend.app.schemas.requests.aimodel import AIModelCreate
from backend.app.schemas.responses.aimodel import EmbeddingModelResponse
from backend.core.factory import Factory

ai_model_router = APIRouter()


@ai_model_router.get("/embedding-model", response_model=EmbeddingModelResponse)
def get_embedding_model(
        ai_model_controller: SettingsController = Depends(Factory().get_ai_model_controller),
) -> EmbeddingModelResponse:
    return ai_model_controller.get_embedding_model()
