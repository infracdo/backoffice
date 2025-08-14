import asyncio
import httpx
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from main import models
from main.library.common import common
from main.schemas.common import PostResponse, GetResponse
from main.core.config import settings
from typing import Optional
from main.library.payconnectInterface import payconnect_interface


class TransactionController:

    async def create_payment_transaction(
        self,
        db: Session,
        current_user: dict,
        payload: dict
    ):

        time_now = common.get_timestamp(1)
        transaction_id = common.uuid_generator()

        try:
            result = await payconnect_interface.get_qr_string(
                transaction_id,
                payload.amount
            )
            if result.get("rawQrString"):
                trans = models.Transaction(
                    type="PAYMENT",
                    status="pending",
                    payment_method=payload.payment_method,
                    amount=payload.amount,
                    qr_code_string=result.get("rawQrString"),
                    user_id=current_user.get("user_id"),
                    transaction_id=transaction_id,
                    created_at=time_now,
                    updated_at=time_now
                )

                db.add(trans)
                db.commit()
                db.refresh(trans)


                return PostResponse(
                    status="ok",
                    status_code=200,
                    message="Payment transaction created successfully.",
                    data={
                        "transaction": jsonable_encoder(trans),
                        "qr_code_string": result.get("rawQrString")
                    }
                ).__dict__
            else:
                return PostResponse(
                    status="error",
                    status_code=500,
                    message="Failed to generate QR",
                    details="Failed to generate QR"
                ).__dict__
        except Exception as e:
            return PostResponse(
                status="error",
                status_code=500,
                message="Failed to generate QR",
                details=str(e)
            ).__dict__

    
    def receive_webhook(
        self,
        db: Session,
        payload: dict
    ):
        print("🔔 Webhook received!")
        print(payload)
        print(f"Result: {payload.result}")
        print(f"Amount: {payload.amount}")
        print(f"retrievalReference: {payload.retrievalReference}")
        print(f"chargeReference: {payload.chargeReference}")

        retval = {
                "errorCode":"0000",
                "errorDescription":"success"
            }
        transaction = (
            db.query(models.Transaction)
            .filter_by(transaction_id=payload.chargeReference)
            .one_or_none()
        )
        if not transaction:
            return retval
        else:
            transaction.updated_at= common.get_timestamp(1)
            transaction.status = "paid"
            transaction.charge_reference = payload.chargeReference
            transaction.retrieval_reference = payload.retrievalReference
            # transaction.amount = payload.amount
            transaction.retrieval_timestamp = payload.timestamp
            db.add(transaction)
            db.commit()
        
        return retval
    

    def payment_transaction_list(
        self,
        db: Session,
        current_user: dict,
        payload: dict,
        search: Optional[str] = None,
        status: Optional[str] = None
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)

        user_id = ""
        if current_user.get("user_id") and \
              current_user.get("user_type") not in ["admin","support"]:
            user_id = current_user.get("user_id")

        filters = []
        if payload.get("id"):
            filters.append(models.Transaction.transaction_id == payload.get("id"))
        
        if search: 
            filters.append(
                or_(
                    models.Transaction.payment_method.ilike(f"%{search}%"),
                    models.Transaction.status.ilike(f"%{search}%"),
                    models.Transaction.type.ilike(f"%{search}%"),
                    models.Transaction.charge_reference.ilike(f"%{search}%"),
                    cast(models.Transaction.amount, String).ilike(search)
                )
            )
        
        if status:
            filters.append(models.Transaction.status == status)

        if user_id:
            filters.append(models.Transaction.user_id == user_id)


        # get total rows count
        data = db.query(models.Transaction).filter(*filters)
        total_rows = data.count()

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        transactions = (
            db.query(models.Transaction, models.User.name)
            .join(models.User, models.Transaction.user_id == models.User.user_id)
            .filter(*filters)
            .order_by(models.Transaction.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        trans_list = []
        for trans, name in transactions:
            print(name)
            trans_dict = trans.__dict__.copy()
            trans_dict["name"] = name
            trans_dict.pop("_sa_instance_state", None)
            trans_list.append(trans_dict)


        return GetResponse(
            status="ok",
            status_code=200,
            data=jsonable_encoder(trans_list),
            total_rows=total_rows
        )


    def download_payment_transaction_list(
        self,
        db: Session,
        filename: str,
        file_type: str,
        search: Optional[str] = None,
        status: Optional[str] = None
    ):
    
        filters = []
 
        if search: 
            filters.append(
                or_(
                    models.Transaction.payment_method.ilike(f"%{search}%"),
                    models.Transaction.status.ilike(f"%{search}%"),
                    models.Transaction.type.ilike(f"%{search}%"),
                    models.Transaction.charge_reference.ilike(f"%{search}%"),
                    cast(models.Transaction.amount, String).ilike(search)
                )
            )

        if status:
            filters.append(models.Transaction.status == status)

        transactions = (
            db.query(models.Transaction, models.User.name)
            .join(models.User, models.Transaction.user_id == models.User.user_id)
            .filter(*filters)
            .order_by(models.Transaction.updated_at.desc())
            .all()
        )

        trans_list = []
        for trans, name in transactions:
            trans_dict = trans.__dict__.copy()
            trans_dict["name"] = name
            trans_dict.pop("_sa_instance_state", None)
            trans_list.append(trans_dict)

        keys = (
            "created_at",
            "updated_at",
            "type",
            "status",
            "payment_method",
            "amount",
            "charge_reference",
            "retrieval_reference",
            "retrieval_timestamp",
            "qr_code_string"
        )
        headers = (
            "Transaction Date",
            "Last Updated",
            "Type",
            "Status",
            "Payment Method",
            "Amount",
            "Charge Reference",
            "Retrieval Reference",
            "Retrieval Timestamp",
            "QR Code String"
        )

        raw_data = {
            "header": keys,
            "headers": headers,
            "rows": jsonable_encoder(trans_list)
        }
        data = common.format_excel(rawData=raw_data)
        return common.get_media_return(
            file_name=filename,
            file_type=file_type,
            data=data,
        )