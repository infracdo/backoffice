from pydantic import BaseModel
from typing import Optional, Union, Dict, List

class CreateRouter(BaseModel):
    business_owner_id: str
    serial_no: str
    router_model: str
    router_version: Optional[str] = None
    mac_address: str
    ip_address: str
    password: str
    qr_string: str
    long: float
    lat: float

class UpdateRouter(BaseModel):
    router_id: str
    owner_user_id: Optional[str] = None
    serial_no: Optional[str] = None
    router_model: Optional[str] = None
    router_version: Optional[str] = None
    mac_address: Optional[str] = None
    ip_address: Optional[str] = None
    password: Optional[str] = None
    qr_string: Optional[str] = None
    data_usage: Optional[float] = None
    subscribers_count: Optional[int] = None
    long: Optional[float] = None
    lat: Optional[float] = None
    is_enabled: Optional [bool] = None


class UpdateRouterUsage(BaseModel):
    router_mac: str
    router_usage: float
    router_subscribers_count: int
    device_id:  str
    device_usage: float