from pydantic import BaseModel, Field


class AIModelCreate(BaseModel):
    llm_model_class: str
    llm_model_name: str
