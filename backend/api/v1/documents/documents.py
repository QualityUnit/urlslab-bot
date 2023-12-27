from fastapi import APIRouter, Depends, Request, UploadFile, File, Form, Security

from backend.app.controllers.document import DocumentController
from backend.app.schemas.extras.completed import Completed
from backend.app.schemas.requests.document import DocumentUpsert
from backend.app.schemas.responses.documents import DocumentResponse
from backend.core.factory import Factory

document_router = APIRouter()


@document_router.get("/{tenant_id}/{document_id}", response_model=DocumentResponse)
async def get_document(
        tenant_id: int,
        document_id: str,
        request: Request,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> DocumentResponse:
    return await document_controller.get_by_id(request.user.id,
                                               tenant_id,
                                               document_id)


@document_router.get("/{tenant_id}", response_model=list[DocumentResponse])
async def get_documents(
        tenant_id: int,
        request: Request,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> list[DocumentResponse]:
    return await document_controller.get_by_tenant_id(request.user.id, tenant_id)


@document_router.post("/upsert/{tenant_id}", response_model=DocumentResponse)
async def upsert_document(
        tenant_id: int,
        request: Request,
        document_upsert: DocumentUpsert,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> DocumentResponse:
    return await document_controller.upsert_single(request.user.id,
                                                   tenant_id,
                                                   document_upsert)


@document_router.post("/upload/{tenant_id}", response_model=DocumentResponse)
async def upload_document_file(
        tenant_id: int,
        request: Request,
        file: UploadFile = File(...),  # PDF or DOCX file
        source: str = Form(None),  # Extra data field
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> DocumentResponse:
    response = await document_controller.upsert_file(request.user.id,
                                                     tenant_id,
                                                     file,
                                                     source)

    return response


@document_router.post("/upsert/bulk/{tenant_id}", response_model=list[DocumentResponse])
async def upsert_documents(
        tenant_id: int,
        request: Request,
        document_upsert: list[DocumentUpsert],
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> list[DocumentResponse]:
    return await document_controller.upsert_bulk(request.user.id,
                                                 tenant_id,
                                                 document_upsert)


@document_router.delete("/{tenant_id}/{document_id}", response_model=Completed)
async def delete_document(
        tenant_id: int,
        request: Request,
        document_id: str,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> Completed:
    await document_controller.delete_by_id(request.user.id, tenant_id, document_id)
    return Completed(status="success")
