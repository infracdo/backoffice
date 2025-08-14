from main.core import deps
from main.modules.transaction.controller import TransactionController
from main.schemas.transaction import CreatePaymentTransaction, PayConnectWebhook
from main.schemas.common import GetPayload, PostResponse
from main.core.security import jwt_required
from main.core.config import settings
from main.library.cosInterface import CosInterface
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Header, Query, UploadFile, File
from typing import Any, Union, Optional, Annotated


router = APIRouter()
controller = TransactionController()

@router.post("/payment",response_model=dict)
async def create_payment_transaction(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    current_user: Annotated[dict, Depends(jwt_required)],
    payload: CreatePaymentTransaction
) -> Any:
    """
        Create Payment Transaction
    """
    return await controller.create_payment_transaction(
        db=db,
        current_user=current_user,
        payload=payload
    )

@router.post("/payment/webhook",response_model=dict)
async def receive_webhook(
    db: Annotated[Session, Depends(deps.get_db)],
    payload: PayConnectWebhook
):
    """
        PayConnect Webhook
    """
    return controller.receive_webhook(
        db=db,
        payload=payload
    )

@router.get('/list')
async def payment_transaction_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    current_user: Annotated[dict, Depends(jwt_required)],
    payload: GetPayload = Depends(),
    search: Annotated[str, Query()] = None,
    status: Annotated[str, Query()] = None,
) -> Any:

    """
    Get Payment Transaction List
    """
    return controller.payment_transaction_list(
        db=db,
        current_user=current_user,
        payload=payload.dict(exclude_none=True),
        search=search,
        status=status
    )

@router.get('/list/download')
async def download_payment_transaction_list(
    db: Annotated[Session, Depends(deps.get_db)],
    *,
    _: Annotated[dict, Depends(jwt_required)],
    filename: str,
    file_type: str,
    search: Annotated[str, Query()] = None,
    status: Annotated[str, Query()] = None
) -> Any:

    """
    Download Payment Transaction List
    """
    return controller.download_payment_transaction_list(
        db=db,
        filename=filename,
        file_type=file_type,
        search=search,
        status=status
    )