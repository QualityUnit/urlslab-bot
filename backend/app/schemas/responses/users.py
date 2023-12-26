from pydantic import UUID4, BaseModel, Field

from backend.app.schemas.extras.token import Token


class UserResponse(BaseModel):
    email: str = Field(..., example="john.doe@example.com")
    username: str = Field(..., example="john.doe")

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    token: Token = Field(..., example="token")
    user: UserResponse = Field(..., example="user")

    class Config:
        from_attributes = True
