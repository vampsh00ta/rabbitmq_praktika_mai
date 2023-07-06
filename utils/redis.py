import aioredis
from aioredis import Redis
from fastapi import Depends
from sqlalchemy.orm.attributes import get_history

from config import REDIS_URL
from src.authv2.auth import get_current_user
from src.authv2.schemas import UserRead
last_seen_count = 10

async def get_async_redis() -> Redis:

    async with aioredis.Redis.from_url(
        REDIS_URL, max_connections=10
    ) as redis:
        yield redis


async def add_last_search(search:str,redis:Redis,user_id:int):
    data = redis.get(f'search_history_{user_id}')
    if not data:
        data = []
    length  = len(data)
    if length == 10 :
        data.append(search)
    else:
        data.insert(length-1,search)
    redis.rpush(f'search_history_{user_id}',*data)
async def get_last_search_history(redis:Redis,user_id:int):
    data = redis.get(f'search_history_{user_id}')
    return data
