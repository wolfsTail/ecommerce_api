from sqlalchemy import insert, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Review, Rating, Product
from app.backend.repositories.base_repo import BaseRepo
from app.backend.utils.exceptions import NoItemError


class ReviewRepository(BaseRepo):
    model_name = Review
    additional_model = Rating

    @classmethod
    async def get_all_reviews_with_rating(cls, db_session: AsyncSession):
        query = select(Review, Rating.value).join(Review.rating).where(Review.is_active == True)
        results = await db_session.execute(query)
        reviews = results.all()
        return reviews
    
    @classmethod
    async def set_average_rating(cls, db_session: AsyncSession, product_id: int):
        avg_query = (
            select(
                func.avg(Rating.value).label("average_rating")
            )
            .select_from(Review)
            .join(Rating, Review.id == Rating.review_id)
            .where(Review.product_id == product_id, Review.is_active == True)
        )

        results = await db_session.execute(query)
        results = results.all()
        return float(results[0].average_rating) if results[0].average_rating else 0.00
    
    @classmethod
    async def get_special_reviews(cls, db_session: AsyncSession, product_id: int):
        reviews_query = (
            select(
                Review.id.label("review_id"),
                Review.comment,
                Review.user_id,
                Review.comment_date,
                func.avg(Rating.value).label("average_rating"),
                Product.rating.label("product_average_rating")  
            )
            .join_from(Review, Rating, Review.id == Rating.review_id)
            .join(Product, Product.id == Review.product_id)  
            .where(Review.product_id == product_id, Review.is_active == True)
            .group_by(Review.id, Product.id)  
        )
        reviews_result = await db_session.execute(reviews_query)
        reviews = reviews_result.all()

        if not reviews:
            raise NoItemError()
        
        return reviews

