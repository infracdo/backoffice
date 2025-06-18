from typing import Optional, Any, Union
from pydantic import BaseModel


class GetTotalsPayload(BaseModel):
    owner_user_id: Optional[str] = None

class GetTotalsResponse(BaseModel):
    status: str
    status_code: Optional[int] = 200
    detail: Optional[str] = None
    total_business_owners: int = 0
    total_routers: int = 0
    total_subscribers: int = 0
    total_data_usage: float = 0

class FilteredByDate(BaseModel):
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    owner_user_id: Optional[str] = None

class GetFilteredByDateResponse(BaseModel):
    status: str
    status_code: Optional[int] = 200
    detail: Optional[str] = None
    total: Optional[Union[int, float]] = 0