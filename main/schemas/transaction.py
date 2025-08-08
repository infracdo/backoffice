from pydantic import BaseModel
from typing import Optional, Union, Dict, List

class CreatePaymentTransaction(BaseModel):
    amount: float = 10.00
    payment_method: str = "QRPH"

class PayConnectWebhook(BaseModel):
    result: str
    retrievalReference: str
    amount: str
    authCode: str
    paymentCode: str = ""
    signature: str
    chargeReference: str
    timestamp: str
    paymentType: str
