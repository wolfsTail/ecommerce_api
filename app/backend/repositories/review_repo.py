from models import Review
from backend.repositories.base_repo import BaseRepo


class ReviewRepository(BaseRepo):
    model_name = Review
