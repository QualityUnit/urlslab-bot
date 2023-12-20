from enum import Enum
from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, String
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


class TenantPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    # Users relation
    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship('User', back_populates="tenants")

    # Chatbots relation
    chatbots = relationship('Chatbot', back_populates="tenant")

    def __acl__(self):
        basic_permissions = [TenantPermission.CREATE]
        self_permissions = [
            TenantPermission.READ,
            TenantPermission.EDIT,
            TenantPermission.DELETE,
        ]
        all_permissions = list(TenantPermission)

        return [
            (Allow, Authenticated, basic_permissions),
            (Allow, UserPrincipal(self.user.id), self_permissions),
            (Allow, RolePrincipal("admin"), all_permissions),
        ]
