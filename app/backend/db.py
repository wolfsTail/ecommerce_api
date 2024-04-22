from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


engine = create_async_engine(
    'postgresql+asyncpg://ecommerce:password@localhost:5432/ecommerce', echo=True
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession) 
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass