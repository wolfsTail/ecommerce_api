from abc import ABC, abstractmethod

from app.backend.repositories import (
    CategoryRepository,
    UserRepository,
    ProductRepository,
    RatingRepository,
    ReviewRepository,
)


class AbstractUnitOfWork(ABC):
    categories: CategoryRepository
    products: ProductRepository
    users: UserRepository
    ratings: RatingRepository
    reviews: ReviewRepository

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass

    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
