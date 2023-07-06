from typing import List

from pydantic import BaseModel
from src.authv2.schemas import UserRead
class Category(BaseModel):
    name:str
    class Config:
        orm_mode = True

class ItemCreate(BaseModel):
    name:str
    price:str
    image:str
    category:List[Category]
    size:str
    brand:str
    used:bool
    class Config:
        orm_mode = True
class Item(ItemCreate):
    id:int
    is_active:bool
    liked_by:List[UserRead]
    class Config:
        orm_mode = True
class LikedBy(BaseModel):
    count:int
    liked_by:List[UserRead]
    class Config:
        orm_mode = True
