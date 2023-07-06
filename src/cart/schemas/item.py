from pydantic import BaseModel
from datetime import datetime
from pydantic.typing import List
from pydantic.typing import ForwardRef


class Item(BaseModel):
    id:int
    name:str
    price:str
    image:str
    class Config:
        orm_mode = True
class ItemRead(BaseModel):
    owner_id:int

# ListItem = ForwardRef("List[ItemRead]")
class DeleteItem(BaseModel):
    id:int
class CartItem(BaseModel):
    name: str
    price: str
    image: str