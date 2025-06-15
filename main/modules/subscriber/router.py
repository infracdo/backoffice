from main.core import deps
from main.modules.subscriber.controller import SubscriberController
from main.schemas.subscriber import CreateSubscriber, UpdateSubscriber, GetByOwner
from main.schemas.common import GetPayload
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from typing import Any, Union, Optional


router = APIRouter()
controller = SubscriberController()

@router.post("/create",response_model=dict)
async def create_subscriber(
    db: Session = Depends(deps.get_db),
    *,
    current_user: dict = Depends(jwt_required),
    payload: CreateSubscriber
) -> Any:
    """
        Create Subscriber
    """
    return controller.create_subscriber(
        db=db,
        current_user=current_user,
        payload=payload.dict(exclude_unset=True)
    )

@router.put("/update",response_model=dict)
async def update_subscriber(
    db: Session = Depends(deps.get_db),
    *,
    _: dict = Depends(jwt_required),
    payload: UpdateSubscriber
) -> Any:
    """
        Update Subscriber
    """
    return controller.update_subscriber(
        db=db,
        payload=payload.dict(exclude_unset=True)
    )

@router.get('/list')
async def subscriber_list(
    db: Session = Depends(deps.get_db),
    *,
    _: dict = Depends(jwt_required),
    payload: GetPayload = Depends(),
) -> Any:

    """
    Get Subscriber List
    """
    return controller.subscriber_list(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.get('/list/by-router-owner')
async def subscriber_list_by_router_owner(
    db: Session = Depends(deps.get_db),
    *,
    _: dict = Depends(jwt_required),
    payload: GetByOwner = Depends(),
) -> Any:

    """
    Get Subscriber List By Router Owner
    """
    return controller.subscriber_list_by_router_owner(
        db=db,
        payload=payload.dict(exclude_unset=True)
    )

@router.delete('/delete')
async def delete_subscriber(
    db: Session = Depends(deps.get_db),
    *,
    _: dict = Depends(jwt_required),
    id: str,
) -> Any:

    """
    Delete Subscriber
    """
    return controller.delete_subscriber(
        db=db,
        id=id
    )