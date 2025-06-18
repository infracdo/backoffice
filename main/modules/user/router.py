from main.core import deps
from main.modules.user.controller import UserController
from main.schemas.user import CreateUser, UpdateUser, \
    CreateTier, UpdateTier
from main.schemas.common import GetPayload
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from typing import Any, Union, Optional, Annotated


router = APIRouter()
controller = UserController()

@router.get('/types')
async def user_types(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: GetPayload = Depends(),
) -> Any:

    """
    Get User Types/Roles
    """
    return controller.user_types(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.get('/tiers')
async def subscriber_tiers(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: GetPayload = Depends(),
) -> Any:

    """
    Get Subscriber Tiers
    """
    return controller.subscriber_tiers(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.post("/tier/create",response_model=dict)
async def create_subscriber_tier(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: CreateTier
) -> Any:
    """
        Create Subscriber Tier
    """
    return controller.create_subscriber_tier(
        db=db,
        payload=payload.dict(exclude_unset=True)
    )

@router.put("/tier/update",response_model=dict)
async def update_subscriber_tier(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: UpdateTier
) -> Any:
    """
        Update Subscriber Tier
    """
    return controller.update_subscriber_tier(
        db=db,
        payload=payload.dict(exclude_unset=True)
    )

@router.delete('/tier/delete')
async def delete_subscriber_tier(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    id: str,
) -> Any:

    """
    Delete Subscriber Tier
    """
    return controller.delete_subscriber_tier(
        db=db,
        id=id
    )

@router.post("/create",response_model=dict)
async def create_user(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: CreateUser
) -> Any:
    """
        Create User
    """
    return controller.create_user(
        db=db,
        payload=payload.dict(exclude_unset=True)
    )

@router.put("/update",response_model=dict)
async def update_user(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: UpdateUser
) -> Any:
    """
        Update User
    """
    return controller.update_user(
        db=db,
        payload=payload.dict(exclude_unset=True)
    )

@router.get('/list')
async def user_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: GetPayload = Depends(),
) -> Any:

    """
    Get User List
    """
    print(payload.limit, payload.page, payload.id)
    return controller.user_list(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.delete('/delete')
async def delete_user(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    id: str,
) -> Any:

    """
    Delete User
    """
    return controller.delete_user(
        db=db,
        id=id
    )