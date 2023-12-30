from fastapi import status, Security
from fastapi.security import APIKeyHeader

from core.config import config
from core.exceptions.base import CustomException, ForbiddenException


class AuthenticationRequiredException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = status.HTTP_401_UNAUTHORIZED
    message = "Authentication required"


class AuthenticationRequired:
    def __init__(
        self,
        api_key: str = Security(APIKeyHeader(name="X-API-Key")),
    ):
        if not api_key:
            raise AuthenticationRequiredException()

        if api_key != config.API_KEY:
            raise ForbiddenException("Invalid API Key")
