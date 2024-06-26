from fastapi import Depends

from app.backend.utils.definite_uow import UnitOfWork
from app.backend.utils.abstract_uow import AbstractUnitOfWork


from app.backend.service import (
    CategoryService,
    ProductService,
    UserService,
    ReviewService,
)


def get_category_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> CategoryService:
    return CategoryService(uow)

def get_product_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> ProductService:
    return ProductService(uow)

def get_user_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> UserService:
    return UserService(uow)

def get_review_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> ReviewService:
    return ReviewService(uow)
