from pydantic import BaseModel
from typing import Optional, Union, Dict, List

class CreateRouter(BaseModel):
    serial_no: str
    router_model: str
    router_version: str
    long: float
    lat: float

class UpdateRouter(BaseModel):
    router_id: str
    owner_user_id: Optional[str] = None
    serial_no: Optional[str] = None
    router_model: Optional[str] = None
    router_version: Optional[str] = None
    data_usage: Optional[float] = None
    subscribers_count: Optional[int] = None
    long: Optional[float] = None
    lat: Optional[float] = None
    is_active: Optional [bool] = None