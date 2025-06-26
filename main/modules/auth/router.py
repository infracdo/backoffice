from main.core import deps
from main.modules.auth.controller import AuthController
from main.schemas.auth import Signin, ForgotPassword, ChangePassword
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from typing import Any, Union, Annotated


router = APIRouter()
controller = AuthController()

@router.post("/signin")
async def signin(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: Signin
) -> Any:
    """
        Signin Authentication
    """
    return controller.sign_in(
        db=db,
        credentials=payload.dict(exclude_unset=True)
    )

@router.put("/forgot-password")
async def forgot_password(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    payload: ForgotPassword
) -> Any:
    """
        Forgot Password
    """
    return controller.forgot_password(
        db=db,
        email=payload.email,
        user_type=payload.user_type
    )

@router.put("/change-password")
async def change_password(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    current_user: Annotated[dict, Depends(jwt_required)],
    payload: ChangePassword
) -> Any:
    """
        Change Password
    """
    return controller.change_password(
        db=db,
        current_user=current_user,
        payload=payload.dict()
    )