from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update
from slugify import slugify
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db_depends import get_db
from app.models import Product, Category, Rating, Review
from app.schemas import CreateProduct, RequestReview
from app.routers.permissions import get_current_user


router = APIRouter(
    prefix="/reviews", 
    tags=["reviews"]
)


@router.get('all_reviews')
async def get_all_reviews(
    db: Annotated[AsyncSession, Depends(get_db)],
):
    query = select(Review, Rating.value).join(Review.rating).where(Review.is_active == True)
    results = await db.execute(query)
    reviews = results.all()

    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no reviews"
        )    

    response = [{
        "review_id": review.id,
        "user_id": review.user_id,
        "product_id": review.product_id, 
        "comment": review.comment, 
        "rating_value": value
        }
        for review, value in reviews
    ]
    return response

@router.post("/add_review")
async def add_review(
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
    review: RequestReview
):
    if get_user.get('is_customer'):
        query = insert(Review).values(
            comment=review.comment,
            user_id=get_user.get('id'),
            product_id=review.product_id,
        ).returning(Review.id)

        review_id = await db.execute(query)      
        review_id = review_id.scalar_one()

        query = select(Review).where(Review.id == review_id)
        review_from_bd = await db.execute(query)
        review_from_bd = review_from_bd.scalar_one()

        query = insert(Rating).values(
            value=review.rating.value,
            user_id=get_user.get('id'),
            product_id=review.product_id,
            review_id=review_from_bd.id,
        )
        await db.execute(query)

        avg_query = (
            select(
                func.avg(Rating.value).label("average_rating")
            )
            .select_from(Review)
            .join(Rating, Review.id == Rating.review_id)
            .where(Review.product_id == review.product_id, Review.is_active == True)
        )

        result = await db.execute(avg_query)
        result = result.all()
        avg_rating = float(result[0].average_rating) if result[0].average_rating else 0.00

        update_product = update(Product).\
                         where(Product.id == review.product_id).\
                         values(rating=avg_rating)
        await db.execute(update_product)

        await db.commit()      

        return {
            "status_code": status.HTTP_200_OK,
            "transaction": 'Succes add a new review and rating',
        }
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You cannot use this method!'
        )

@router.get('/products_reviews/{product_slug}')
async def products_reviews(
    db: Annotated[AsyncSession, Depends(get_db)],
    product_slug: str,
):
    query = select(Product).where(Product.slug == product_slug)
    product = await db.scalar(query)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    reviews_query = (
            select(
                Review.id.label("review_id"),
                Review.comment,
                Review.user_id,
                Review.comment_date,
                func.avg(Rating.value).label("average_rating"),
                Product.rating.label("product_average_rating")  # Общий средний рейтинг продукта
            )
            .join_from(Review, Rating, Review.id == Rating.review_id)
            .join(Product, Product.id == Review.product_id)  # Джоиним таблицу Product для доступа к общему рейтингу
            .where(Review.product_id == product.id, Review.is_active == True)
            .group_by(Review.id, Product.id)  # Группируем также по Product.id для корректности агрегации
        )
    reviews_result = await db.execute(reviews_query)
    reviews = reviews_result.all()

    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="There are no active reviews for this product"
        )

    response = {
        "product_id": product.id,
        "reviews": [
            {
                "review_id": review.review_id,
                "comment": review.comment,
                "user_id": review.user_id,
                "comment_date": review.comment_date.isoformat(),
                "average_rating": float(review.product_average_rating) if review.product_average_rating else None
            }
            for review in reviews
        ]
    }

    return response


@router.delete('/delete_reviews')
async def delete_reviews(
    db: Annotated[AsyncSession, Depends(get_db)],
    get_user: Annotated[dict, Depends(get_current_user)],
    review_id: int
):
    if get_user.get('is_admin'):
        query = select(Review).where(Review.id == review_id)
        review = await db.scalar(query)
        
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found!"
        )
        active_query = update(Review).where(Product.id == review.id).values(is_active=False)
        await db.execute(active_query)

        active_query = update(Rating).where(Rating.review_id == review.id).values(is_active=False)
        await db.execute(active_query)

        await db.commit()

        return {
                "status_code": status.HTTP_200_OK,
                "transaction": 'Review and rating delete successful',
            }
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not authorized to use this method'
        )

