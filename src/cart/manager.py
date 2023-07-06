import functools

from fastapi import HTTPException
from sqlalchemy import select

from src.authv2.models import Item


# async def if_owner_adder(session:AsyncSession = Depends(get_async_session)):
#     item_owner_query = select(Item).where(Item.id == item.id ).where(Item.owner_id ==user_data.id)
#
#     item_owner = (await session.execute(item_owner_query)).scalar()
#         if item_owner:
#             raise HTTPException(status_code=403,detail={'status':'cant add yourself item'})


def if_can_add_item(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        user_data =  kwargs['user_data']
        item = kwargs['item']
        session = kwargs['session']
        item_owner_query = select(Item).where(Item.id == item.id).where(Item.owner_id == user_data.id)
        item_owner = (await session.execute(item_owner_query)).scalar()
        if item_owner:
            raise HTTPException(status_code=403, detail={'status': 'cant add yourself item'})
        return await func(*args, **kwargs)

    return wrapper


