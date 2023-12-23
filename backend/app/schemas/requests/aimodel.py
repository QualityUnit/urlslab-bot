from pydantic import BaseModel, Field


class AIModelCreate(BaseModel):
    chat_model_class: str
    chat_model_name: str
