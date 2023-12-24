from typing import Callable
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from starlette.responses import StreamingResponse

from backend.app.controllers import TenantController
from backend.app.controllers.session import SessionController
from backend.app.models.tenant import TenantPermission
from backend.app.schemas.extras.completed import Completed
from backend.app.schemas.requests.chat import ChatCompletionRequest

from backend.app.schemas.responses.session import SessionResponse
from backend.app.schemas.responses.tenants import TenantResponse
from backend.core.exceptions import BadRequestException
from backend.core.factory import Factory
from backend.core.fastapi.dependencies.permissions import Permissions

session_router = APIRouter()


@session_router.post("/{session_id}/stream", response_model=list[TenantResponse])
async def stream_chatbot_response(
        session_id: str,
        request: Request,
        chat_completion_request: ChatCompletionRequest,
        session_controller: SessionController = Depends(Factory().get_session_controller),
) -> StreamingResponse:
    try:
        UUID(session_id)
    except ValueError:
        raise BadRequestException("Invalid session id")

    return StreamingResponse(
        session_controller.stream_chatbot_response(request.user.id, UUID(session_id), chat_completion_request),
        media_type="text/event-stream")


@session_router.put("/{tenant_id}/{chatbot_id}", response_model=SessionResponse, status_code=201)
async def create_session(
        tenant_id: int,
        chatbot_id: int,
        request: Request,
        session_controller: SessionController = Depends(Factory().get_session_controller),
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        assert_access: Callable = Depends(Permissions(TenantPermission.READ)),
) -> SessionResponse:
    tenant = await tenant_controller.get_by_id(tenant_id)
    assert_access(tenant)

    return await session_controller.create_session(request.user.id, tenant_id, chatbot_id)


@session_router.delete("/{session_id}", response_model=Completed)
async def delete_session(
        session_id: str,
        request: Request,
        session_controller: SessionController = Depends(Factory().get_session_controller),
) -> Completed:
    try:
        UUID(session_id)
    except ValueError:
        raise BadRequestException("Invalid session id")
    session_controller.delete_session(request.user.id, UUID(session_id))
    return Completed(status="success")