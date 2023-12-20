from fastapi import APIRouter

from .monitoring import monitoring_router
from .users import users_router
from .tenants import tenants_router

v1_router = APIRouter()
v1_router.include_router(monitoring_router, prefix="/monitoring")
v1_router.include_router(users_router, prefix="/users")
v1_router.include_router(tenants_router, prefix="/tenants")
