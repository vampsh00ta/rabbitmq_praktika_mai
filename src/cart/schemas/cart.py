from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime
from pydantic.typing import ForwardRef
class CartItem(BaseModel):
    name: str
    price: str
    image: str
class Cart(BaseModel):
    id:CartItem