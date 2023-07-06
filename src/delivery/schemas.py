from typing import List, Union

from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime
from pydantic.typing import ForwardRef


class DeliveryCreateSchema(BaseModel):
    track_id:int
    receiver_name:str
    telephone_number:str
    street:str
    city:str
    class Config:
        orm_mode = True

class UpdateDeliveryStatusSchema(BaseModel):
    track_id:int
    delivery_status:int
    city:str
    class Config:
        orm_mode = True
class DeliveryStatusNameRead(BaseModel):
    name:str
    class Config:
        orm_mode = True
class DeliveryStatusRead(BaseModel):
    current_city:str
    delivery_status:DeliveryStatusNameRead
    status_update:datetime
    class Config:
        orm_mode = True
class DeliveryUserRead(BaseModel):
    track_id:int
    receiver_name:str
    telephone_number:str
    street:str
    city:str
    is_deliveried:bool
    dilivery_day:Union[datetime,None]
    statuses:List[DeliveryStatusRead]
    class Config:
        orm_mode = True



