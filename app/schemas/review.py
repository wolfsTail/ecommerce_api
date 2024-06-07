from pydantic import BaseModel

from app.schemas.rating import InnerRating


class RequestReview(BaseModel):
    product_id: int
    comment: str
    rating: InnerRating | None = None