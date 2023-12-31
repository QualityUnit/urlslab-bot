from enum import Enum

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from core.database import Base
from core.database.mixins import TimestampMixin


class TenantPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class Tenant(Base, TimestampMixin):
    __tablename__ = "tenants"

    id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

    # Chatbots relation
    chatbots = relationship('Chatbot', backref="tenant")
