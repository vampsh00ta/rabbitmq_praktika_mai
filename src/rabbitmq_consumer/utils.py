from sqlalchemy.ext.asyncio import AsyncSession

from src.delivery.models import Delivery,Status
import uuid
from datetime import datetime,timedelta

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
          instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper
# async def create_delivery(delivery_data:dict,session:AsyncSession):
#     delivery = Delivery(**delivery_data)
#     delivery.track_id = uuid.uuid1()
#     delivery.dilivery_day = datetime.utcnow() + timedelta(days=2)
#     session.add(delivery)
#     await session.commit()
