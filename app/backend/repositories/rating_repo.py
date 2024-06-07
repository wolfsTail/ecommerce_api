from app.models import Rating
from app.backend.repositories.base_repo import BaseRepo


class RatingRepository(BaseRepo):
    model_name = Rating
