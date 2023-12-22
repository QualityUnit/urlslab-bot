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


class Chatbot(Base, TimestampMixin):
    __tablename__ = "chatbots"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    system_prompt = Column(Text, nullable=False)

    # Tenant relation
    tenant_id = Column(
        BigInteger, ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )

    __mapper_args__ = {"eager_defaults": True}

    def __acl__(self):
        raise ValueError("Chatbots Permissions are managed by tenants.")
