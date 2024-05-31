from fastapi import Depends

from app.backend.db_depends import get_db
from app.backend.utils.abstract_uow import AbstractUnitOfWork
from app.backend.utils.depends import (
    get_caregory_repo,
    get_product_repo,
    get_rating_repo,
    get_review_repo,
    get_user_repo,
)
from app.backend.repositories import (
    CategoryRepository,
    UserRepository,
    ProductRepository,
    RatingRepository,
    ReviewRepository,
)


class UnitOfWork(AbstractUnitOfWork):
    categories: CategoryRepository = Depends(get_caregory_repo)
    products: ProductRepository = Depends(get_product_repo)
    users: UserRepository = Depends(get_user_repo)
    ratings: RatingRepository = Depends(get_rating_repo)
    reviews: ReviewRepository = Depends(get_review_repo)

    async def __aenter__(self):
        self.session = Depends(get_db)     

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
