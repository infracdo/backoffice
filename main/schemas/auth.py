from pydantic import BaseModel
from typing import Optional, Union

class Signin(BaseModel):
    email: str
    password: str

class ForgotPassword(BaseModel):
    email: str

class ChangePassword(BaseModel):
    new_password: str
    old_password: str
