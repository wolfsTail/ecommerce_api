from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from app.backend.repositories.base_repo import BaseRepo


class ProductRepository(BaseRepo):
    model_name = Product

    @classmethod
    async def get_all(
        cls, db_session: AsyncSession,
        ) -> list[model_name]:
        query = select(cls.model_name).where(Product.is_active == True, Product.stock > 0)
        result = await db_session.execute(query)
        return result.mappings().all()
    
    @classmethod
    async def get_products_by_categories(
        cls, db_session: AsyncSession, categories: list[int]
        ) -> list[model_name]:
        query = select(Product).where(
        Product.is_active == True, 
        Product.stock > 0, 
        Product.category_id.in_(categories)
        )
        result = await db_session.execute(query)
        return result.mappings().all()
