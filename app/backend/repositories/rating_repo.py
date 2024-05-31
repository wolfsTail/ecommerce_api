from models import Rating
from backend.repositories.base_repo import BaseRepo


class RatingRepository(BaseRepo):
    model_name = Rating
