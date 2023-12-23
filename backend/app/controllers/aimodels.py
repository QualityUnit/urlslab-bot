from backend.app.repositories.aimodels import SettingsRepository
from backend.app.schemas.responses.aimodel import AIModelResponse
from backend.core.exceptions import NotFoundException


class SettingsController:
    def __init__(self, settings_repository: SettingsRepository):
        self.settings_repository = settings_repository

    def get_ai_model(self, user_id: int):
        rsp = self.settings_repository.get_by_id(user_id)
        if rsp is None:
            return NotFoundException("AI Model not found")
        return AIModelResponse(**rsp.__dict__)

    def upsert(self, llm_model_class: str, llm_model_name: str, user_id: int) -> AIModelResponse:
        aimodel = self.settings_repository.get_by_id(user_id)
        aimodel.llm_model_class = llm_model_class
        aimodel.llm_model_name = llm_model_name

        self.settings_repository.upsert(user_id, aimodel)
        return AIModelResponse(**aimodel.__dict__)


