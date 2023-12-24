from datetime import datetime
from typing import Optional
from uuid import UUID

import langchain
import langchain_core
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

from backend.app.models.aimodel import AIModel


class ChatSession:

    def __init__(self,
                 user_id: int,
                 tenant_id: int,
                 chatbot_id: int,
                 ai_model_settings: AIModel,
                 message_history: list[BaseMessage],
                 created_at: datetime,
                 session_id: Optional[UUID] = None):
        self.session_id = session_id or UUID()
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.chatbot_id = chatbot_id
        self.ai_model_settings = ai_model_settings
        self.message_history = message_history
        self.created_at = created_at

    def to_dict(self):
        return {
            "session_id": str(self.session_id),
            "user_id": self.user_id,
            "tenant_id": self.tenant_id,
            "chatbot_id": self.chatbot_id,
            "ai_model_settings": self.ai_model_settings.to_dict(),
            "message_history": [self._base_message_to_dict(message) for message in self.message_history],
            "created_at": self.created_at.strftime("%Y-%m-%d, %H:%M:%S")
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            session_id=UUID(data.get("session_id")),
            user_id=data.get("user_id"),
            tenant_id=data.get("tenant_id"),
            chatbot_id=data.get("chatbot_id"),
            ai_model_settings=AIModel(**data.get("ai_model_settings")),
            message_history=[cls._base_message_from_dict(message) for message in data.get("message_history")] or [],
            created_at=datetime.strptime(data.get("created_at"), "%Y-%m-%d, %H:%M:%S")
        )

    def get_created_at_string(self):
        return self.created_at.strftime("%Y-%m-%d, %H:%M:%S")

    @staticmethod
    def _base_message_to_dict(message: BaseMessage):
        return {
            "content": message.content,
            "baseMessageClass": message.__class__.__name__,
        }

    @staticmethod
    def _base_message_from_dict(data: dict):
        # Ensure the class name is part of the langchain module
        base_message_model = data.get("baseMessageClass")
        if base_message_model in langchain_core.messages.__all__:
            # Get the class object from the module based on the string
            msg_class = getattr(langchain_core.messages, base_message_model)

            # Create an instance of the class
            langchain_msg_class = msg_class(content=data.get("content"))
            return langchain_msg_class
        else:
            raise ValueError(f"Base Message class {base_message_model} is not supported")

    class Config:
        from_attributes = True
