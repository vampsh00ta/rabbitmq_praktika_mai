from random import randint

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.delivery.models import Delivery

#penis
def slatt():
    pass
async def make_unique_track_id(n:int,session:AsyncSession):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    track_id = randint(range_start, range_end)
    track_id_from_db = select(Delivery).where(Delivery.track_id == track_id)
    if (await session.execute(track_id_from_db)).scalar() is not None:
        await make_unique_track_id(n,session)
    return track_id

