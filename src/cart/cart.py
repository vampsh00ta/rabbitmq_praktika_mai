import json

from fastapi import HTTPException, Depends

from aioredis import Redis
from src.authv2.schemas import UserRead
from utils.redis import get_async_redis
from src.cart.schemas.item import Item
from src.cart.schemas.cart import Cart as CartSchema
from src.authv2.models import User
from src.authv2.auth import get_current_user


async def get_items(redis:Redis = Depends(get_async_redis),user:User = Depends(get_current_user))->CartSchema:
    cart = Cart(redis,user)
    await cart.init()
    return await cart.getItems()
async def cartInit(redis:Redis,user:UserRead):
    cart = Cart(redis, user)
    await cart.init()
    return cart

class Cart:
    def __init__(self,redis:Redis,user:UserRead):
        self._redis = redis
        self.user = user


    async def init(self):
        cart = await self._redis.get(f"cart_{self.user.id}")
        if  cart:
            cart =  json.loads(cart)
        else:
            cart = {}
        self.cart = cart

    async def add(self,item:Item):
        product_id = item.id
        await self.check_item_in_cart(item)
        self.cart[product_id] = {
            "name":item.name,
            "price":item.price,
            "image":item.image
        }
        await self.save()
    async def check_item_in_cart(self,item):
        if item.id in self.cart:
            raise HTTPException(
            status_code=403,
            detail='already in cart',
        )
    async def save(self):

        cart =  json.dumps(self.cart).encode('utf-8')
        await self._redis.set(f"cart_{self.user.id}",cart)

    async def remove(self, item):
        product_id = str(item.id)
        if product_id in self.cart:
            del self.cart[product_id]
            await self.save()

    async def deleteCart(self):
        await self._redis.delete(f"cart_{self.user.id}")

    async def getItems(self):
        return self.cart



