from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@postgres/mydatabase"

engine = create_async_engine(DATABASE_URL, echo=True)
engine.execution_options(isolation_level="AUTOCOMMIT")


AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def get_db_for_middleware() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


Base = declarative_base()
