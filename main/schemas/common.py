from typing import Optional, Any
from pydantic import BaseModel

class PostResponse(BaseModel):
    status: str
    status_code: Optional[int] = 200
    message: Optional[str] = None
    detail: Optional[str] = None #for error exception
    data: Optional[dict] = None

class GetResponse(BaseModel):
    status: str
    status_code: Optional[int] = 200
    detail: Optional[str] = None
    data: Optional[Any] = []
    total_rows: Optional[int] = 0

class GetPayload(BaseModel):
    limit: Optional[int] = None
    page: Optional[int] = None
    id: Optional[str] = None


class GetResponseWithDataUsage(BaseModel):
    status: str
    status_code: Optional[int] = 200
    detail: Optional[str] = None
    data: Optional[Any] = []
    total_rows: Optional[int] = 0
    total_data_usage: float

class OTPRequest(BaseModel):
    mobile_no: str
    device_id: str

class OTPResponse(BaseModel):
    status: str
    status_code: Optional[int] = 200
    detail: Optional[str] = None
    otp: str
