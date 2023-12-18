from fastapi import APIRouter

from backend.app.schemas.extras.health import Health
from backend.core.config import config

health_router = APIRouter()


@health_router.get("/")
async def health() -> Health:
    return Health(version=config.RELEASE_VERSION, status="Healthy")
