from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.controllers import TenantController
from app.controllers.document import DocumentController
from app.schemas.extras.completed import Completed
from app.schemas.requests.document import DocumentUpsert
from app.schemas.responses.documents import DocumentResponse
from core.factory import Factory

document_router = APIRouter()


@document_router.get("/{tenant_id}/{document_id}", response_model=DocumentResponse)
async def get_document(
        tenant_id: str,
        document_id: str,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> DocumentResponse:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    return await document_controller.get_by_id(tenant_id,
                                               document_id)


@document_router.get("/{tenant_id}", response_model=list[DocumentResponse])
async def get_documents(
        tenant_id: str,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> list[DocumentResponse]:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    return await document_controller.get_by_tenant_id(tenant_id)


@document_router.post("/upsert/{tenant_id}", response_model=DocumentResponse)
async def upsert_document(
        tenant_id: str,
        document_upsert: DocumentUpsert,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> DocumentResponse:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    return await document_controller.upsert_single(tenant_id,
                                                   document_upsert)


@document_router.post("/global-doc/upsert", response_model=DocumentResponse)
async def upsert_global_document(
        document_upsert: DocumentUpsert,
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> DocumentResponse:
    return await document_controller.upsert_single(None,
                                                   document_upsert)


@document_router.post("/upload/{tenant_id}", response_model=DocumentResponse)
async def upload_document_file(
        tenant_id: str,
        file: UploadFile = File(...),  # PDF or DOCX file
        source: str = Form(None),  # Extra data field
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> DocumentResponse:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    response = await document_controller.upsert_file(tenant_id,
                                                     file,
                                                     source)

    return response


@document_router.post("/upsert/bulk/{tenant_id}", response_model=list[DocumentResponse])
async def upsert_documents(
        tenant_id: str,
        document_upsert: list[DocumentUpsert],
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> list[DocumentResponse]:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    return await document_controller.upsert_bulk(tenant_id,
                                                 document_upsert)


@document_router.delete("/{tenant_id}/{document_id}", response_model=Completed)
async def delete_document(
        tenant_id: str,
        document_id: str,
        tenant_controller: TenantController = Depends(Factory().get_tenant_controller),
        document_controller: DocumentController = Depends(Factory().get_document_controller),
) -> Completed:
    # 404 if tenant does not exist
    await tenant_controller.get_by_id(tenant_id)

    await document_controller.delete_by_id(tenant_id, document_id)
    return Completed(status="success")
