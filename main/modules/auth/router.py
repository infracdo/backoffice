from main.core import deps
from main.modules.auth.controller import AuthController
from main.schemas.auth import Signin, ForgotPassword, ChangePassword
from main.core.security import jwt_required
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header
from typing import Any, Union


router = APIRouter()
controller = AuthController()

@router.post("/signin",response_model=dict)
async def signin(
    db: Session = Depends(deps.get_db),
    *,
    payload: Signin
) -> Any:
    """
        Signin Authentication
    """
    return controller.sign_in(
        db=db,
        credentials=payload.dict(exclude_unset=True)
    )

@router.put("/forgot-password",response_model=dict)
async def forgot_password(
    db: Session = Depends(deps.get_db),
    *,
    payload: ForgotPassword
) -> Any:
    """
        Forgot Password
    """
    return controller.forgot_password(
        db=db,
        email=payload.email
    )

@router.put("/change-password",response_model=dict)
async def change_password(
    db: Session = Depends(deps.get_db),
    *,
    current_user: dict = Depends(jwt_required),
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