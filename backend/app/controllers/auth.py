from uuid import uuid4

from pydantic import EmailStr

from backend.app.models import User
from backend.app.models.aimodel import AIModel
from backend.app.repositories import UserRepository
from backend.app.repositories.aimodels import SettingsRepository
from backend.app.repositories.document import DocumentRepository
from backend.app.schemas.extras.token import Token
from backend.app.schemas.responses.users import LoginResponse, UserResponse
from backend.core.controller import BaseController
from backend.core.exceptions import BadRequestException, UnauthorizedException
from backend.core.security import JWTHandler, PasswordHandler


class AuthController(BaseController[User]):
    def __init__(self,
                 user_repository: UserRepository,
                 settings_repository: SettingsRepository,
                 document_repository: DocumentRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository
        self.settings_repository = settings_repository
        self.document_repository = document_repository

    async def register(self, email: EmailStr, password: str, username: str) -> User:
        # Check if user exists with email
        user = await self.user_repository.get_by_email(email)

        if user:
            raise BadRequestException("User already exists with this email")

        # Check if user exists with username
        user = await self.user_repository.get_by_username(username)

        if user:
            raise BadRequestException("User already exists with this username")

        password = PasswordHandler.hash(password)

        user = await self.user_repository.create(
            {
                "email": email,
                "password": password,
                "username": username,
            }
        )

        # Creating default ai models
        user_ai_model = AIModel.default()
        self.settings_repository.upsert(user.id, user_ai_model)

        # Creating Index in Vector Database
        await self.document_repository.create_document_index(user.id, user_ai_model)

        return user

    async def login(self, email: EmailStr, password: str) -> LoginResponse:
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise BadRequestException("Invalid credentials")

        if not PasswordHandler.verify(user.password, password):
            raise BadRequestException("Invalid credentials")

        token = Token(
            access_token=JWTHandler.encode(payload={"user_id": user.id}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )

        return LoginResponse(
            token=token,
            user=UserResponse(**user.__dict__),
        )

    def refresh_token(self, access_token: str, refresh_token: str) -> Token:
        token = JWTHandler.decode(access_token)
        refresh_token = JWTHandler.decode(refresh_token)
        if refresh_token.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        return Token(
            access_token=JWTHandler.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )
