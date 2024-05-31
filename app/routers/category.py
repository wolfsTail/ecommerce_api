from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update
from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models import Category
from app.schemas import CreateCategory, ResponseCategory
from app.routers.auth import get_current_user
from app.backend.service import CategoryService
from app.backend.utils.depends import get_category_service


router = APIRouter(
    prefix='/category',
    tags=['category']
)

@router.get(
        '/all_categories',         
        )
async def get_all_categories(
    service: CategoryService = Depends(get_category_service)
    ):
    categories = await service.get_all()
    if categories:
        return categories
    raise HTTPException(status_code=404, detail="Не найдено ни одной категории")
   

@router.post('/create')
async def create_category(
    db: Annotated[AsyncSession, Depends(get_db)], 
    create_category: CreateCategory,
    get_user: Annotated[dict, Depends(get_current_user)]
    ) -> dict:
    if get_user.get('is_admin'):
        await db.execute(
            insert(Category).values(
                name=create_category.name,
                parent_id=create_category.parent_id,
                slug=slugify(create_category.name)
            )
        )
        await db.commit()

        return {
            "status_code": status.HTTP_201_CREATED,
            "transaction": "OK!"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='You have not any credentials for create a category!'
    )        

@router.put('/update_category')
async def update_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    category_id: int,
    update_category: CreateCategory,
    get_user: Annotated[dict, Depends(get_current_user)]
    ):
    if get_user.get('is_admin'):
        query = select(Category).where(Category.id == category_id)
        category = await db.scalar(query)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found!"
            )
        
        active_query = update(Category).where(Category.id == category_id).values(
            name=update_category.name, parent_id=update_category.parent_id
        )
        await db.execute(active_query)
        await db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Category update succes!"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='You have not any credentials for create a category!'
    ) 

@router.delete('/delete')
async def delete_category(
    db: Annotated[AsyncSession, Depends(get_db)],
    category_id: int,
    get_user: Annotated[dict, Depends(get_current_user)]
    ):
    if get_user.get('is_admin'):
        query = select(Category).where(Category.id == category_id)
        category = await db.scalar(query)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found!"
            )
        
        active_query = update(Category).where(Category.id == category_id).values(is_active=False)
        await db.execute(active_query)
        await db.commit()
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": "Delete succes!"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='You have not any credentials for create a category!'
    ) 
