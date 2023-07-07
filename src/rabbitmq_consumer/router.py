import asyncio
import json
import uuid
from datetime import datetime, timedelta

from aio_pika import IncomingMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from config import logger
import logging

from src.delivery.models import Delivery, Status, StatusName

# logger = logging.getLogger(__name__)

class DeliveryRouter(object):
    async def create_delivery(self,delivery_data: dict, get_session):
        async with get_session() as session:
            delivery = Delivery(**delivery_data)
            delivery.dilivery_day = datetime.utcnow() + timedelta(days=2)
            session.add(delivery)
            status_name_q = select(StatusName).where(StatusName.name.like('обрабатывается'))
            status_name = (await session.execute(status_name_q)).scalar()
            await session.flush()

            status = Status(current_city = 'Unknown',
                            last_update = datetime.utcnow(),
                            track_id = delivery.track_id,
                            delivery_status_name = status_name.id)
            session.add(status)
            await session.commit()
