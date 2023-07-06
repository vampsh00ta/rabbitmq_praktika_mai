from typing import List

from pydantic import BaseModel
from datetime import datetime

from pydantic.typing import ForwardRef

from src.cart.schemas.item import Item
from src.cart.schemas.order import Order


class UserOrdersItems(BaseModel):
    id:int
    username:str
    registered_at:datetime
    updated_at:datetime
    orders:List[Order]
    items:List[Item]
    class Config:
        orm_mode = True
