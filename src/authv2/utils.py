from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy.ext.asyncio import AsyncSession

from utils.database import get_async_session
from .models import User

async def async_get_user(session:AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session,User)