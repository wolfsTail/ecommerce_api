from fastapi import Depends

from app.backend.utils.definite_uow import UnitOfWork
from app.backend.utils.abstract_uow import AbstractUnitOfWork
from app.backend.repositories import (
    CategoryRepository,
    ProductRepository,
    UserRepository,
    ReviewRepository,
    RatingRepository,
)
from app.backend.service import (
    CategoryService,
)


def get_category_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> CategoryService:
    return CategoryService(uow)

def get_caregory_repo() -> CategoryRepository:
    return CategoryRepository

def get_user_repo() -> UserRepository:
    return UserRepository

def get_product_repo() -> ProductRepository:
    return ProductRepository

def get_review_repo() -> ReviewRepository:
    return ReviewRepository

def get_rating_repo() -> RatingRepository:
    return RatingRepository
