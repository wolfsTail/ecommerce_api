from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from app.backend.db_depends import get_db
from app.models import Category
from app.schemas import CreateCategory, ResponseCategory, UpdateCategory
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
    service: Annotated[CategoryService, Depends(get_category_service)]
    ):
    categories = await service.get_all()
    if categories:
        return categories
    raise HTTPException(status_code=404, detail="Не найдено ни одной категории")


@router.post('/create')
async def create_category(
    creating_category: CreateCategory,
    get_user: Annotated[dict, Depends(get_current_user)],
    service: Annotated[CategoryService, Depends(get_category_service)],
):
    result = await service.create_category(
        creating_category, get_user
    )
    if not result:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='You have not any credentials for create a category!'
    )
    return result


@router.put('/update')
async def update_category(
    updating_category: UpdateCategory,
    get_user: Annotated[dict, Depends(get_current_user)],
    service: Annotated[CategoryService, Depends(get_category_service)],
):
    result = await service.update_category(
        updating_category, get_user
    )
    if not result:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found!"
    )
    if isinstance(result, int):
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='You have not any credentials for create a category!'
    )
    return result


@router.delete('/delete')
async def delete_category(
    category_id: int, 
    get_user: Annotated[dict, Depends(get_current_user)],
    service: Annotated[CategoryService, Depends(get_category_service)]
):
    result = await service.delete_category(category_id, get_user)
    if not result:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Category not found!"
    )
    if not isinstance(result, bool):
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='You have not any credentials for create a category!'
    )
    return result
