from pydantic import BaseModel
from typing import Optional, Union

class Signin(BaseModel):
    email_or_mobile_no: str
    password: str

class ForgotPassword(BaseModel):
    email: str

class ChangePassword(BaseModel):
    new_password: str
    old_password: str
