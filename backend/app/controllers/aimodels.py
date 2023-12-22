from backend.app.repositories.aimodels import AIModelRepository


class AIModelController:
    def __init__(self, ai_model_repository: AIModelRepository):
        self.ai_model_repository = ai_model_repository

    def get_ai_model(self, user_id: int):
        return self.ai_model_repository.get_by_id(user_id)

    def upsert(self, llm_model_class: str, llm_model_name: str, user_id: int):
        aimodel = self.ai_model_repository.get_by_id(user_id)
        aimodel.llm_model_class = llm_model_class
        aimodel.llm_model_name = llm_model_name

        return self.ai_model_repository.upsert(user_id, aimodel)


