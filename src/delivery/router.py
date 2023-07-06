import datetime

from fastapi import APIRouter, Depends
import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.delivery.models import Delivery,Status,StatusName
from src.delivery.schemas import DeliveryCreateSchema, UpdateDeliveryStatusSchema, DeliveryUserRead
from utils.database import get_async_session

router  = APIRouter(
    prefix = '/delivery',
    tags=['delivery']

)




#
# @router.post('/createDelivery')
# async def create_delivery(delivery_data:DeliveryCreateSchema,session:AsyncSession = Depends(get_async_session)):
#     delivery = Delivery(**delivery_data.__dict__)
#     # track_id= make_random_track_id(9)
#
#     delivery_status = DeliveryStatus(current_city =delivery_data.city,delivery_status_id =1 ,status_update = datetime.datetime.utcnow(),track_id =track_id  )
#     session.add(delivery)
#     session.add(delivery_status)
#     await session.commit()

@router.post('/updateDelivery')
async def update_delivery(delivery_data:UpdateDeliveryStatusSchema,session:AsyncSession = Depends(get_async_session)):

    # delivery_status_model = select(DeliveryStatusName).where(DeliveryStatus.id == delivery_data.status)
    status= Status(current_city = delivery_data.city,
                           delivery_status_id = delivery_data.delivery_status,
                           status_update = datetime.datetime.utcnow(),
                           track_id = delivery_data.track_id
                           )

    session.add(status)
    await session.commit()
    return 200

@router.get('/getDeliveryStatus/{track_id}',response_model=DeliveryUserRead)
async def get_delivery_status(track_id:int,session:AsyncSession = Depends(get_async_session)):
    delivery_model_query =  select(Delivery).where(Delivery.track_id == track_id)
    delivery = (await session.execute(delivery_model_query)).scalar()
    return DeliveryUserRead.from_orm(delivery)
# @router.post('/get')
# async def update_delivery(delivery_data:UpdateDeliveryStatusSchema,session:AsyncSession = Depends(get_async_session)):
#
#     # delivery_status_model = select(DeliveryStatusName).where(DeliveryStatus.id == delivery_data.status)
#     status= Status(current_city = delivery_data.city,
#                            delivery_status = delivery_data.delivery_status,
#                            status_update = datetime.datetime.utcnow(),
#                            track_id = delivery_data.track_id
#                            )
#
#     session.add(status)
#     await session.commit()
#     return 200

