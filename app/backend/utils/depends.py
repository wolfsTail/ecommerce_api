from fastapi import Depends

from app.backend.utils.definite_uow import UnitOfWork
from app.backend.utils.abstract_uow import AbstractUnitOfWork
from app.backend.repositories.depends import (
    get_category_repo,
    get_product_repo,
    get_rating_repo,
    get_review_repo,
    get_user_repo,
)

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

