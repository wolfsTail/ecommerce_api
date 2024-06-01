from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update
from slugify import slugify
from app.backend.db_depends import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category
from app.schemas import CreateCategory, ResponseCategory, UpdateCategory
from app.routers.auth import get_current_user
from app.backend.utils.abstract_uow import AbstractUnitOfWork



class CategoryService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def get_all(self) -> list[Category]:
        filters = {
            "is_active": True,
        }
        async with self.uow:
            categories = await self.uow.categories.get_by_filter(
                filters=filters, db_session=self.uow.session)
            if categories:
                response = categories
                return response
            return []
    
    async def create_category(
            self, category: CreateCategory, get_user: dict,
            ):
        if get_user.get("is_admin"):
            category = category.model_dump()
            async with self.uow:
                new_category = await self.uow.categories.create_one(
                    category, self.uow.session,
                )
            return new_category

    async def update_category(
            self, category: UpdateCategory, get_user: dict,
    ):
        if get_user.get("is_admin"):
            category: dict = category.model_dump()
            categoty_id = category.pop("id")
            async with self.uow:
                updated_category = await self.uow.categories.update_one(
                    categoty_id, self.uow.session, category
                )
            return updated_category 
        return -1

    async def delete_category(
            self, category_id: int, get_user: dict,
    ) -> bool | int:
        if get_user.get("is_admin"):
            async with self.uow:
                flag = await self.uow.categories.delete_one(
                    category_id, self.uow.session,
                )
            return flag
        return -1
