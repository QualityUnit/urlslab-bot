from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from backend.core.database import Base
from backend.core.database.mixins import TimestampMixin
from backend.core.security.access_control import (
    Allow,
    Authenticated,
    RolePrincipal,
    UserPrincipal,
)


class ChatbotPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Chatbot(Base, TimestampMixin):
    __tablename__ = "chatbots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    system_prompt = Column(Text, nullable=False)

    # Tenant relation
    tenant_id = Column(
        BigInteger, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    tenant = relationship('Tenant', back_populates="chatbots")

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        basic_permissions = [ChatbotPermission.CREATE]
        self_permissions = [
            ChatbotPermission.READ,
            ChatbotPermission.EDIT,
            ChatbotPermission.DELETE,
        ]
        all_permissions = list(ChatbotPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.tenant.user_id), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
