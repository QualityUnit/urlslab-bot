from typing import Callable

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.controllers import AuthController, UserController
from backend.app.models.user import User, UserPermission
from backend.app.schemas.extras.token import Token
from backend.app.schemas.requests.users import LoginUserRequest, RegisterUserRequest
from backend.app.schemas.responses.users import UserResponse
from backend.core.factory import Factory
from backend.core.fastapi.dependencies import AuthenticationRequired
from backend.core.fastapi.dependencies.current_user import get_current_user

user_router = APIRouter()


@user_router.post("/", status_code=201)
async def register_user(
    register_user_request: RegisterUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> UserResponse:
    return await auth_controller.register(
        email=register_user_request.email,
        password=register_user_request.password,
        username=register_user_request.username,
    )


@user_router.post("/login")
async def login_user(
    login_user_request: LoginUserRequest,
    auth_controller: AuthController = Depends(Factory().get_auth_controller),
) -> Token:
    return await auth_controller.login(
        email=login_user_request.email, password=login_user_request.password
    )


@user_router.get("/me", dependencies=[Depends(AuthenticationRequired)])
def get_user(
    user: User = Depends(get_current_user),
) -> UserResponse:
    return user
