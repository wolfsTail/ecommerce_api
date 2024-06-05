from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.utils.depends import get_review_service
from app.models import Product, Rating, Review
from app.schemas import RequestReview
from app.routers.permissions import get_current_user
from app.backend.service import ReviewService
from app.backend.utils.exceptions import (
    YouAreNotAdmin,
    NoItemError,
    NoUserError,
    IncorrectCredentailsError,
    NotTheBuyerOfProduct,
    NoItemError,
    NoProductBySlugError,
    YouAreNotAdmin,
)


router = APIRouter(
    prefix="/reviews", 
    tags=["reviews"]
)


@router.get('all_reviews')
async def get_all_reviews(
    service: Annotated[ReviewService, Depends(get_review_service)],
):  
    try:
        reviews = await service.get_reviews()
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
    except (NoItemError) as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )
    

@router.post("/add_review")
async def add_review(
    service: Annotated[ReviewService, Depends(get_review_service)],
    get_user: Annotated[dict, Depends(get_current_user)],
    review: RequestReview,
):
    try:
        transaction = await service.add_review(
            review, get_user
        )
        return {
            "status_code": status.HTTP_200_OK,
            "transaction": transaction,
        }
    except NotTheBuyerOfProduct as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )

@router.get('/products_reviews/{product_slug}')
async def products_reviews(
    service: Annotated[ReviewService, Depends(get_review_service)],
    product_slug: str,
):
    try:
        reviews = await service.get_products_reviews(product_slug)

        response = {
            "product_slug": product_slug,
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
    except (NoItemError,
        NoProductBySlugError) as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
            )

@router.delete('/delete_reviews')
async def delete_reviews(
    service: Annotated[ReviewService, Depends(get_review_service)],
    get_user: Annotated[dict, Depends(get_current_user)],
    review_id: int
):
    try:
        await service.delete_review(get_user, review_id)
        return {
                "status_code": status.HTTP_200_OK,
                "transaction": 'Review delete successful',
            }
    except (YouAreNotAdmin, NoItemError) as err:
        raise HTTPException(
            status_code=err.descr, detail=err.detail
        )
