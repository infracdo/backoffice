from main.core import deps
from main.modules.dashboard.controller import DashboardController
from main.schemas.dashboard import GetCountsPayload, UpdateOnline
from main.schemas.common import GetPayload
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, Query
from typing import Any, Union, Optional, Annotated


router = APIRouter()
controller = DashboardController()


@router.get('/count')
async def get_count(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: GetCountsPayload = Depends(), 
) -> Any:

    """
    Get Total Counts
    """
    return controller.get_count(
        db=db,
        payload=payload.dict(exclude_none=True),
    )

@router.get('/online')
async def get_online(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
) -> Any:

    """
    Get Total Online
    """
    return controller.get_online(
        db=db,
    )

@router.get('/data')
async def get_data(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
) -> Any:

    """
    Get Dashboard Data
    """
    return controller.get_data(
        db=db
    )



@router.put("/update",response_model=dict)
async def update_realtime_data(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: UpdateOnline
) -> Any:
    """
        Update Realtime Data
    """
    return controller.update_realtime_data(
        db=db,
        payload=payload.dict(exclude_none=True)
    )