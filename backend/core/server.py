from typing import List

from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from api import router
from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    SQLAlchemyMiddleware,
)
from core.utils.version_manager import VersionManager


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def custom_generate_unique_id(route: APIRoute):
    return f"{route.name}"


def initial_security_check():
    # checking api key
    if config.ENV != "dev" and config.API_KEY == "dev-key":
        raise Exception("API_KEY is not set")


def create_app() -> FastAPI:
    # update steps and init
    if config.ENV == "prod":
        version_manager = VersionManager()
        version_manager.setup()

    initial_security_check()

    app_ = FastAPI(
        title="URLsLab Bot",
        description="URLsLab Bot for chatbot",
        version="1.0.0",
        docs_url=None if config.ENV == "prod" else "/docs",
        redoc_url=None if config.ENV == "prod" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
        generate_unique_id_function=custom_generate_unique_id,
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


app = create_app()
