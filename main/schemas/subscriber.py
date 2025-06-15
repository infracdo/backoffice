from pydantic import BaseModel
from typing import Optional, Union, Dict, List

class CreateSubscriber(BaseModel):
    router_id: str

class UpdateSubscriber(BaseModel):
    subscriber_id: str
    user_id: Optional[str] = None
    router_id: Optional[str] = None
    data_usage: Optional[float] = None

class GetByOwner(BaseModel):
    limit: Optional[int] = None
    page: Optional[int] = None
    owner_user_id: str