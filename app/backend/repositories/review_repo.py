from app.models import Review
from app.backend.repositories.base_repo import BaseRepo


class ReviewRepository(BaseRepo):
    model_name = Review
