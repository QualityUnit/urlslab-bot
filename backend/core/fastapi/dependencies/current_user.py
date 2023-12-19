from fastapi import Depends, Request

from backend.app.controllers.user import UserController
from backend.core.factory import Factory


def get_current_user(
    request: Request,
    user_controller: UserController = Depends(Factory().get_user_controller),
):
    return user_controller.get_by_id(request.user.id)
