import datetime

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from config import RABBITMQ_QUEUE_KEY_RECOMMENDATIONS, RABBITMQ_QUEUE_KEY_DELIVERY
from utils.database import get_async_session
from src.authv2.auth import get_current_user, get_user_model
from src.authv2.models import  User
from src.authv2.schemas import UserRead
from src.cart.cart import get_items,cartInit
from src.cart.models import Order
from utils.producer import producer
from utils.redis import get_async_redis
from src.cart.schemas.item import Item as ItemSchema, DeleteItem
from src.items.models import Item
from src.cart.schemas.order import Order as OrderSchema, MakeOrder
from src.cart.schemas.user import  UserOrdersItems
from src.cart.schemas.cart import Cart as CartSchema
# from src.recommendations.rec import recsInit

router = APIRouter(
    prefix = "/cart",
    tags = [" cart"]
)


@router.post('/items/{item_id}')
# @if_can_add_item
async def add_to_cart(
    # item:ItemSchema,
    item_id:int,
    session:AsyncSession = Depends(get_async_session),
    user_data:UserRead = Depends(get_current_user),
    redis: Redis = Depends(get_async_redis)

)-> ItemSchema:

    item_query =  select(Item).where(Item.id == item_id)
    item = (await session.execute(item_query)).scalar()

    if item.owner_id == user_data.id    :
        raise HTTPException(status_code=403, detail={'status': 'cant add yourself item'})
    if not  item.is_active:
        raise HTTPException(status_code=403, detail={'status': 'item inactive'})

    cart = await cartInit(redis,user_data)
    await cart.add(item)
    return item.__dict__
@router.delete('/items')
async def delete_from_cart(
    item:DeleteItem,
    user:UserRead = Depends(get_current_user),
    redis: Redis = Depends(get_async_redis)

)-> JSONResponse:

    cart = await cartInit(redis,user)
    await  cart.remove(item)

    return JSONResponse(content={"status":'ok'},status_code=200)
@router.get('/items')
async def get_cart(
    # redis:Redis = Depends(get_async_redis),
    # user:UserRead = Depends(get_current_user),
    cart:CartSchema = Depends(get_items))-> CartSchema:
    return JSONResponse(cart,status_code=200)

@router.post('/order',response_model=OrderSchema)
async def order(order_data:MakeOrder,
                redis:Redis = Depends(get_async_redis),
                user:User = Depends(get_user_model),
                session:AsyncSession = Depends(get_async_session),
        user_data:UserRead = Depends(get_current_user)):
    cart = await cartInit(redis, user_data)
    cart_data = await cart.getItems()
    if not cart_data:
        raise HTTPException(status_code=403,detail="empty cart")
    order = Order()
    session.add(order)
    await session.commit()
    order_query = select(Order).where(Order.id == order.id)
    order = (await session.execute(order_query)).scalar()


    for item_id in cart_data:
        query = select(Item).where(Item.id == int(item_id))
        item = (await session.execute(query)).scalars().first()
        item.is_active  =False
        item.change_item = datetime.datetime.utcnow()
        order.items.append(item)
    user.orders.append(order)
    #recommendation topic
    await producer.send_default(key=RABBITMQ_QUEUE_KEY_RECOMMENDATIONS, data={
        "user_id": user.id,
        "tags": (item.brand + ' ' + item.name).split(' '),
        'type': 'purchases',
        'category': item.category[0].name

    })

    # delivery topic
    await producer.send_default(key=RABBITMQ_QUEUE_KEY_DELIVERY, data=order_data.json())
    await session.commit()

    # await cart.deleteCart()
    return order

@router.get("/userInfo",response_model=UserOrdersItems)
async def user_info(user:User = Depends(get_user_model))->UserOrdersItems:

    return user.__dict__

