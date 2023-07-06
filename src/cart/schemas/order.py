from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime
from src.cart.schemas.item import Item
from pydantic.typing import ForwardRef
from typing import List

class MakeOrder(BaseModel):
    email:str = 'test'
    street:str = 'test'
class MakeOrder(BaseModel):
    receiver_name:str = 'test'
    telephone_number: str = 'test'
    street:str = 'test'
    city:str = 'test'
    class Config:
        orm_mode = True



class Order(BaseModel):
    id:int
    date:datetime
    items:List[Item]
    class Config:
        orm_mode = True

# ListOrder= ForwardRef("List[Order]")
