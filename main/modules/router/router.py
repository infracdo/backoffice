from main.core import deps
from main.modules.router.controller import RouterController
from main.schemas.router import CreateRouter, UpdateRouter
from main.schemas.common import GetPayload
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from typing import Any, Union, Optional


router = APIRouter()
controller = RouterController()

@router.post("/create",response_model=dict)
async def create_router(
    db: Session = Depends(deps.get_db),
    *,
    current_user: dict = Depends(jwt_required),
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
    db: Session = Depends(deps.get_db),
    *,
    _: dict = Depends(jwt_required),
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
    db: Session = Depends(deps.get_db),
    *,
    _: dict = Depends(jwt_required),
    payload: GetPayload = Depends(), 
) -> Any:

    """
    Get Router List
    """
    return controller.router_list(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.delete('/delete')
async def delete_router(
    db: Session = Depends(deps.get_db),
    *,
    _: dict = Depends(jwt_required),
    id: str,
) -> Any:

    """
    Delete Router
    """
    return controller.delete_router(
        db=db,
        id=id
    )