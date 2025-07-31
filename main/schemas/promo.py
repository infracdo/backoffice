from pydantic import BaseModel
from typing import Optional, Union, Dict, List

class CreatePromo(BaseModel):
    image_url: str
    link_url: str
    title: str
    type: str
    description: Optional[str] = None
    is_show: bool = True 


class UpdatePromo(BaseModel):
    promo_id: str
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    is_show: Optional[bool] = None
