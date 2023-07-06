from typing import AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import DB_PASSWORD,DB_PORT,DB_NAME,DB_HOST,DB_USER
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"







engine = create_async_engine(DATABASE_URL,poolclass=NullPool)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


