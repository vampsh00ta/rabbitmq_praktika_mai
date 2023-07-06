from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from utils.database import get_async_session
from .auth import AuthService
from .schemas import UserRead
from .utils import User


from fastapi import Depends, Request


async def get_current_user(request:Request)->UserRead:
    data = AuthService.validate(request)
    return data

async def get_user_model(session:AsyncSession = Depends(get_async_session),
                         user:UserRead = Depends(get_current_user)) ->User:
    username = user.username
    query = select(User).where(User.username == username)
    user = (await session.execute(query)).scalars().first()
    return user
