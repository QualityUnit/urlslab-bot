from fastapi import APIRouter, Depends, Request

from backend.app.controllers.aimodels import AIModelController
from backend.app.schemas.requests.aimodel import AIModelCreate
from backend.app.schemas.responses.aimodel import AIModelResponse
from backend.core.factory import Factory

ai_model_router = APIRouter()


@ai_model_router.get("/", response_model=AIModelResponse)
def get_used_model(
        request: Request,
        ai_model_controller: AIModelController = Depends(Factory().get_ai_model_controller),
) -> AIModelResponse:
    return ai_model_controller.get_ai_model(request.user.id)


@ai_model_router.post("/", response_model=AIModelResponse)
def upsert_ai_model(
        request: Request,
        ai_model_create: AIModelCreate,
        ai_model_controller: AIModelController = Depends(Factory().get_ai_model_controller),
) -> AIModelResponse:
    return ai_model_controller.upsert(ai_model_create.llm_model_class,
                                      ai_model_create.llm_model_name,
                                      request.user.id)