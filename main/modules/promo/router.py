from main.core import deps
from main.modules.promo.controller import PromoController
from main.schemas.promo import CreatePromo, UpdatePromo
from main.schemas.common import GetPayload, PostResponse
from main.core.security import jwt_required
from main.core.config import settings
from main.library.cosInterface import CosInterface
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, Query, UploadFile, File
from typing import Any, Union, Optional, Annotated

cos = CosInterface(
    api_key=settings.IBM_COS_API_KEY,
    service_instance_id=settings.IBM_COS_SERVICE_INSTANCE_ID,
    bucket_name=settings.IBM_COS_BUSCKET_NAME,
    region=settings.IBM_COS_REGION
)


router = APIRouter()
controller = PromoController()

@router.post('/upload/file')
async def upload_file(
    *,
    file: UploadFile = File(...),
) -> Any:


    # VALIDATE FILE
    if not file:
        return PostResponse(
                status="error",
                status_code=400,
                message="File not found",
                detail="Failed. File not found"
            ).__dict__
    
    result = cos.upload_fileobj(file.file, f"promos/{file.filename}")

    if result["success"]:
        return PostResponse(
                status="ok",
                status_code=200,
                message="File uploaded successfully",
                data={ "url": result["url"] }
            ).__dict__
    else:
        return PostResponse(
                status="error",
                status_code=400,
                message="File uploading failed",
                detail=result["error"]
            ).__dict__


@router.post("/create",response_model=dict)
async def create_promo(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: CreatePromo
) -> Any:
    """
        Create Promo
    """
    return controller.create_promo(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.put("/update",response_model=dict)
async def update_promo(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: UpdatePromo
) -> Any:
    """
        Update Promo
    """
    return controller.update_promo(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.get('/list')
async def promo_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: GetPayload = Depends(), 
    type: Annotated[str, Query()] = None,
    is_all: Annotated[bool, Query()] = False,
    search: Annotated[str, Query()] = None
) -> Any:

    """
    Get Promo List
    """
    return controller.promo_list(
        db=db,
        payload=payload.dict(exclude_none=True),
        type=type,
        is_all=is_all,
        search=search
    )

@router.get('/list/download')
async def download_promo_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    filename: str,
    file_type: str,
    type: Annotated[str, Query()] = None,
    is_all: Annotated[bool, Query()] = False,
    search: Annotated[str, Query()] = None,
    
) -> Any:

    """
    Download Promo List
    """
    return controller.download_promo_list(
        db=db,
        filename=filename,
        file_type=file_type,
        type=type,
        is_all=is_all,
        search=search
    )

@router.delete('/delete')
async def delete_promo(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    id: str,
) -> Any:

    """
    Delete Promo
    """
    return controller.delete_promo(
        db=db,
        id=id
    )