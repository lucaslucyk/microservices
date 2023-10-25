from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)

from core.config import settings


# async sqlite session
async_engine: AsyncEngine = create_async_engine(
    settings.DB_URI,
    future=True,
    connect_args={"check_same_thread": False}
)

AsyncSessionLocal: AsyncSession = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)