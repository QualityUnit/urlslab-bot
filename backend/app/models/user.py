from enum import Enum
from typing import List
from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Column, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped

from backend.core.database import Base
from backend.core.database.mixins import TimestampMixin
from backend.core.security.access_control import Allow, Everyone, RolePrincipal, UserPrincipal


class UserPermission(Enum):
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(Unicode(255), nullable=False, unique=True)
    password = Column(Unicode(255), nullable=False)
    username = Column(Unicode(255), nullable=False, unique=True)
    tenants = relationship('Tenant', backref='user')

    def __acl__(self):
        basic_permissions = [UserPermission.READ, UserPermission.CREATE]
        self_permissions = [
            UserPermission.READ,
            UserPermission.EDIT,
            UserPermission.CREATE,
        ]
        all_permissions = list(UserPermission)

        return [
            (Allow, Everyone, basic_permissions),
            (Allow, UserPrincipal(value=self.id), self_permissions),
            (Allow, RolePrincipal(value="admin"), all_permissions),
        ]
