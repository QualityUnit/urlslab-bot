from sqlalchemy import BigInteger, Column, ForeignKey, String, Text

from app.models.aimodel import UrlslabChatModel
from core.database import Base
from core.database.mixins import TimestampMixin


class Chatbot(Base, TimestampMixin):
    __tablename__ = "chatbots"

    id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    system_prompt = Column(Text, nullable=False)
    chat_model_class = Column(String(255), nullable=False)
    chat_model_name = Column(String(255), nullable=False)

    # Tenant relation
    tenant_id = Column(
        String(255), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )

    __mapper_args__ = {"eager_defaults": True}

    def chatbot_model(self) -> UrlslabChatModel:
        return UrlslabChatModel(
            chat_model_class=self.chat_model_class,
            chat_model_name=self.chat_model_name,
        )
