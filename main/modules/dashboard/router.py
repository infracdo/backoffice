from main.core import deps
from main.modules.dashboard.controller import DashboardController
from main.schemas.dashboard import GetTotalsPayload
from main.schemas.common import GetPayload
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, Query
from typing import Any, Union, Optional, Annotated


router = APIRouter()
controller = DashboardController()


@router.get('/list')
async def router_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: GetTotalsPayload = Depends(), 
) -> Any:

    """
    Get Totals
    """
    return controller.get_totals(
        db=db,
        payload=payload.dict(exclude_none=True),
    )