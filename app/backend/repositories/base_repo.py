from abc import ABC, abstractclassmethod

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update


class AbstractRepo(ABC):
    @classmethod
    @abstractclassmethod
    async def get_one(cls, item_id: int, db_session: AsyncSession):
        raise NotImplemented("This is a abstractclass method")
    
    @classmethod
    @abstractclassmethod
    async def get_all(cls, db_session: AsyncSession):
        raise NotImplemented("This is a abstractclass method")
    
    @classmethod
    @abstractclassmethod
    async def create_one(cls, data: dict, db_session: AsyncSession):
        raise NotImplemented("This is a abstractclass method")
    
    @classmethod
    @abstractclassmethod
    async def update_one(cls, item_id: int, data: dict, db_session: AsyncSession):
        raise NotImplemented("This is a abstractclass method")
    
    @classmethod
    @abstractclassmethod
    async def delete_one(cls, item_id: int, db_session: AsyncSession):
        raise NotImplemented("This is a abstractclass method")


class BaseRepo:
    model_name = None

    @classmethod
    async def get_one(
        cls, item_id: int, db_session: AsyncSession
        ) -> model_name:
        stmt = select(cls.model_name).filter_by(id=item_id)
        result = await db_session.execute(stmt)
        return result.scalar_one_or_none()
    
    @classmethod
    async def get_by_filter(
        cls, filters: dict, db_session: AsyncSession
    ) -> list[model_name]:
        stmt = select(cls.model_name).filter_by(**filters)
        result = await db_session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_all(
        cls, db_session: AsyncSession,
        ) -> list[model_name]:
        stmt = select(cls.model_name)
        result = await db_session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def create_one(
        cls, data: dict, db_session: AsyncSession 
        ) -> model_name:
        stmt = insert(cls.model_name).values(**data).returning(cls.model_name)
        result = await db_session.execute(stmt)
        return result.scalar_one()

    @classmethod
    async def update_one(
        cls, item_id:int, db_session: AsyncSession, data: dict
        ) -> model_name:
        stmt = (
            update(cls.model_name)
            .where(cls.model_name.id == item_id)
            .values(**data)
            .returning(cls.model_name)
        )
        result = await db_session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def delete_one(cls, item_id: int, db_session: AsyncSession) -> bool:
        stmt = delete(cls.model_name).where(cls.model_name.id == item_id)
        result = await db_session.execute(stmt)
        return bool(result.rowcount)