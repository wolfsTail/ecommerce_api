from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update
from slugify import slugify
from app.backend.db_depends import get_db

from app.models import Category
from app.schemas import CreateCategory


router = APIRouter(
    prefix='/category',
    tags=['category']
)

@router.get('/all_categories')
async def get_all_categories(db: Annotated[Session, Depends(get_db)]):
    query = select(Category).where(Category.is_active == True)
    categories = db.scalars(query).all()
    return categories    

@router.post('/create')
async def create_category(
    db: Annotated[Session, Depends(get_db)], create_category: CreateCategory
    ) -> dict:
    db.execute(
        insert(Category).values(
            name=create_category.name,
            parent_id=create_category.parent_id,
            slug=slugify(create_category.name)
        )
    )
    db.commit()

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "OK!"
    }

@router.put('/update_category')
async def update_category(
    db: Annotated[Session, Depends(get_db)],
    category_id: int,
    update_category: CreateCategory,
    ):
    query = select(Category).where(Category.id == category_id)
    category = db.scalar(query)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found!"
        )
    
    active_query = update(Category).where(Category.id == category_id).values(
        name=update_category.name, parent_id=update_category.parent_id
    )
    db.execute(active_query)
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Category update succes!"
    }

@router.delete('/delete')
async def delete_category(
    db: Annotated[Session, Depends(get_db)],
    category_id: int
    ):
    query = select(Category).where(Category.id == category_id)
    category = db.scalar(query)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found!"
        )
    
    active_query = update(Category).where(Category.id == category_id).values(is_active=False)
    db.execute(active_query)
    db.commit()
    return {
        "status_code": status.HTTP_200_OK,
        "transaction": "Delete succes!"
    }
