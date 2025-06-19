from pydantic import BaseModel, EmailStr
from typing import Optional, Union, Dict, List

class UserBase(BaseModel):
    name: str
    mobile_no: str
    email: EmailStr
    user_type: str
    is_active: bool = True  # default active

class CreateUser(UserBase):
    password: str  # required on creation
    device_id: Optional[str] = None
    will_return_token: bool = False

class UpdateUser(BaseModel):
    user_id: str
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    user_type: Optional[str] = None
    is_active: Optional[bool] = None
    device_id: Optional[str] = None
    data_limit: Optional[float] = None
    data_usage: Optional[float] = None
    tier: Optional[str] = None

class CreateTier(BaseModel):
    name: str
    description: Optional[str] = None
    data_limit: float
    is_default_tier: bool = False

class UpdateTier(BaseModel):
    tier_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    data_limit: Optional[float] = None
    is_default_tier: Optional[bool] = None
