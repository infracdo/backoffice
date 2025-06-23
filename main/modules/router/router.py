from main.core import deps
from main.modules.router.controller import RouterController
from main.schemas.router import CreateRouter, UpdateRouter
from main.schemas.common import GetPayload
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, Query
from typing import Any, Union, Optional, Annotated


router = APIRouter()
controller = RouterController()

@router.post("/create",response_model=dict)
async def create_router(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    current_user: Annotated[dict, Depends(jwt_required)],
    payload: CreateRouter
) -> Any:
    """
        Create Router
    """
    return controller.create_router(
        db=db,
        current_user=current_user,
        payload=payload.dict(exclude_none=True)
    )

@router.put("/update",response_model=dict)
async def update_router(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: UpdateRouter
) -> Any:
    """
        Update Router
    """
    return controller.update_router(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.get('/list')
async def router_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: GetPayload = Depends(), 
    with_total_data_usage: Annotated[bool, Query()] = False,
    with_total_subscribers: Annotated[bool, Query()] = False,
    search: Annotated[str, Query()] = None,
    business_owner_id: Annotated[str, Query()] = None
) -> Any:

    """
    Get Router List
    """
    return controller.router_list(
        db=db,
        payload=payload.dict(exclude_none=True),
        with_total_data_usage=with_total_data_usage,
        with_total_subscribers=with_total_subscribers,
        search=search,
        business_owner_id=business_owner_id
    )

@router.get('/list/download')
async def download_router_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    filename: str,
    file_type: str,
    search: Annotated[str, Query()] = None,
    
) -> Any:

    """
    Download Router List
    """
    return controller.download_router_list(
        db=db,
        filename=filename,
        file_type=file_type,
        search=search
    )

@router.delete('/delete')
async def delete_router(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    id: str,
) -> Any:

    """
    Delete Router
    """
    return controller.delete_router(
        db=db,
        id=id
    )