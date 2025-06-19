from main.core import deps
from main.modules.otp.controller import OtpController
from main.schemas.common import OTPRequest, GetPayload
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from typing import Any, Union, Optional, Annotated


router = APIRouter()
controller = OtpController()

@router.post('/send')
async def send_otp(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: OTPRequest = Depends(),
) -> Any:

    """
    Send OTP
    """
    return controller.send_otp(
        db=db,
        payload=payload.dict(exclude_none=True)
    )

@router.get('/list')
async def sent_otp_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: GetPayload = Depends(),
) -> Any:

    """
    Get Sent OTP List
    """
    return controller.sent_otp_list(
        db=db,
        payload=payload.dict(exclude_none=True),
    )