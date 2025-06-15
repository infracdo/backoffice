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
    will_return_token: bool = False

class UpdateUser(BaseModel):
    user_id: str
    name: Optional[str] = None
    mobile_no: Optional[str] = None
    email: Optional[EmailStr] = None
    user_type: Optional[str] = None
    is_active: Optional[bool] = None

