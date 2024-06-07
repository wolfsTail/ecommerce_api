from app.backend.utils.abstract_uow import AbstractUnitOfWork

from app.schemas import RequestReview
from app.backend.utils.exceptions import (
    YouAreNotAdmin,
    NoItemError,
    NotTheBuyerOfProduct,
    NoProductBySlugError,
    YouAreNotAdmin,
)


class ReviewService:
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def get_reviews(self):
        async with self.uow:
            reviews = await self.uow.reviews.get_all_reviews_with_rating(self.uow.session)

            if not reviews:
                raise NoItemError
            
            return reviews
    
    async def add_review(
            self, review: RequestReview, get_user: dict
    ):
        values_review = {
            "comment": review.comment,
            "user_id": get_user.get('id'),
            "product_id": review.product_id,
        }
        async with self.uow:
            if get_user.get('is_customer'):
                review_bd = await self.uow.reviews.create_one(
                    values_review, self.uow.session
                )
                values_rating = {
                    "value": review.rating.value,
                    "user_id": get_user.get('id'),
                    "product_id": review.product_id,
                    "review_id": review_bd.id,
                }

                rating = await self.uow.ratings.create_one(
                    values_rating, self.uow.session
                )
                avg_rating = await self.uow.reviews.set_average_rating(
                    self.uow.session, review.product_id
                )
                await self.uow.products.update_one(
                    review.product_id, self.uow.session, {"rating": avg_rating}
                )
                return "Success"
            raise NotTheBuyerOfProduct
    
    async def get_products_reviews(
            self, product_slug: str
    ):
        async with self.uow:
            filters = {
                "slug": product_slug,
            }
            product = await self.uow.products.get_by_filter(
                filters, self.uow.session,
            ).first()
            if not product:
                raise NoProductBySlugError
            return  await self.uow.reviews.get_special_reviews(
                self.uow.session, product.id
            )
    
    async def delete_review(
            self, get_user: dict, review_id: int
    ):
        async with self.uow:
            if get_user.get('is_admin'):
                result = await self.uow.reviews.delete_one(
                    review_id, self.uow.session
                )
                if not result:
                    raise NoItemError
                return result
            raise YouAreNotAdmin
