from fastapi import APIRouter

from .documents import documents_router
from .monitoring import monitoring_router
from .sessions import sessions_router
from .settings import settings_router
from .users import users_router
from .tenants import tenants_router
from .chatbots import chatbots_router

v1_router = APIRouter()
v1_router.include_router(monitoring_router, prefix="/monitoring")
v1_router.include_router(users_router, prefix="/users")
v1_router.include_router(tenants_router, prefix="/tenants")
v1_router.include_router(chatbots_router, prefix="/chatbots")
v1_router.include_router(settings_router, prefix="/settings")
v1_router.include_router(documents_router, prefix="/documents")
v1_router.include_router(sessions_router, prefix="/sessions")
