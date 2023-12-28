from backend.app.repositories.aimodels import SettingsRepository
from backend.app.schemas.responses.aimodel import EmbeddingModelResponse
from backend.core.exceptions import NotFoundException


class SettingsController:
    def __init__(self, settings_repository: SettingsRepository):
        self.settings_repository = settings_repository

    def get_embedding_model(self):
        rsp = self.settings_repository.get_embedding_model()
        if rsp is None:
            return NotFoundException("AI Model not found")
        return EmbeddingModelResponse(**rsp.to_dict())

