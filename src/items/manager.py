
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.database import get_async_session
from src.items.models import Item


async def get_items_model(id:int = None,session:AsyncSession = Depends(get_async_session)):
    query = select(Item).where(Item.id == id)
    if id:
        result = (await session.execute(query)).scalar()
    else:
        result = (await session.execute(query)).scalars().all()

    return result